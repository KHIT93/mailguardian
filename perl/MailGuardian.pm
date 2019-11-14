#
# MailGuardian for MailScanner
# Copyright (C) 2003-2011  Steve Freegard (steve@freegard.name)
# Copyright (C) 2011  Garrod Alwood (garrod.alwood@lorodoes.com)
# Copyright (C) 2014-2017  MailWatch Team (https://github.com/MailWatch/1.2.0/graphs/contributors)
# Copyright (C) 2018 @KHIT93 (https://github.com/khit93/mailguardian/contributers.md)
#
#   Custom Module MailGuardian
#
#   Version 1.0
#
# This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# In addition, as a special exception, the copyright holder gives permission to link the code of this program with
# those files in the PEAR library that are licensed under the PHP License (or with modified versions of those files
# that use the same license as those files), and distribute linked combinations including the two.
# You must obey the GNU General Public License in all respects for all of the code used other than those files in the
# PEAR library that are licensed under the PHP License. If you modify this program, you may extend this exception to
# your version of the program, but you are not obligated to do so.
# If you do not wish to do so, delete this exception statement from your version.
#
# You should have received a copy of the GNU General Public License along with this program; if not, write to the Free
# Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

package MailScanner::CustomConfig;

use strict;
use DBI;
use utf8;
use Data::UUID;
use Sys::Hostname;
use Storable(qw[freeze thaw]);
use POSIX;
use Socket;
use Encoding::FixLatin qw(fix_latin);
use Digest::SHA1;

# Uncommet the folloging line when debugging MailGuardian.pm
#use Data::Dumper;

use vars qw($VERSION);

### The package version, both in 1.23 style *and* usable by MakeMaker:
$VERSION = substr q$Revision: 1.0 $, 10;

# Trace settings - uncomment this to debug
#DBI->trace(2,'/tmp/dbitrace.log');

my ($dbh);
my ($sth_mail);
my ($hostname) = hostname;
my $loop = inet_aton("127.0.0.1");
my $server_port = 11553;
my $timeout = 3600;
my $ug = Data::UUID->new;

# Get database information from MailGuardianConf.pm
use File::Basename;
my $dirname = dirname(__FILE__);
require $dirname.'/MailGuardianConf.pm';

my ($db_name) = MailGuardian_get_db_name();
my ($db_host) = MailGuardian_get_db_host();
my ($db_user) = MailGuardian_get_db_user();
my ($db_pass) = MailGuardian_get_db_password();

sub InitMailGuardianLogging {
    # Detect if MailScanner Milter is calling this custom function and do not spawn
    # MSMilter uses the blacklists and whitelists, but not the logger
    if ($0 !~ /MSMilter/) {
        my $pid = fork();
        if ($pid) {
            # MailScanner child process
            waitpid $pid, 0;
            MailScanner::Log::InfoLog("MailWatch: Started MailGuardian SQL Logging child");
        } else {
            # New process
            # Detach from parent, make connections, and listen for requests
            POSIX::setsid();
            if (!fork()) {
                $SIG{HUP} = $SIG{INT} = $SIG{PIPE} = $SIG{TERM} = $SIG{ALRM} = \&ExitLogging;
                alarm $timeout;
                $0 = "MailGuardian SQL";
                InitConnection();
                ListenForMessages();
            }
        exit;
        }
    }
}

sub InitConnection {
    # Set up TCP/IP socket.  We will start one server per MailScanner
    # child, but only one child will actually be able to get the socket.
    # The rest will die silently.  When one of the MailScanner children
    # tries to log a message and fails to connect, it will start a new
    # server.
    socket(SERVER, PF_INET, SOCK_STREAM, getprotobyname("tcp"));
    setsockopt(SERVER, SOL_SOCKET, SO_REUSEADDR, 1);
    my $addr = sockaddr_in($server_port, $loop);
    bind(SERVER, $addr) or exit;
    listen(SERVER, SOMAXCONN) or exit;

    # Our reason for existence - the persistent connection to the database
    $dbh = DBI->connect("DBI:Pg:database=$db_name;host=$db_host",
        $db_user, $db_pass,
        { PrintError => 0, AutoCommit => 1, RaiseError => 1 }
    );
    if (!$dbh) {
        MailScanner::Log::WarnLog("MailGuardian: Unable to initialise database connection: %s", $DBI::errstr);
    }
    # $dbh->do('SET NAMES utf8mb4');
}

sub ExitLogging {
    # Server exit - commit changes, close socket, and exit gracefully.
    close(SERVER);
    $dbh->disconnect;
    exit;
}

sub ListenForMessages {
    my $message;
    # Wait for messages
    while (my $cli = accept(CLIENT, SERVER)) {
        my ($port, $packed_ip) = sockaddr_in($cli);
        my $dotted_quad = inet_ntoa($packed_ip);

        # Reset emergency timeout - if we haven"t heard anything in $timeout
        # seconds, there is probably something wrong, so we should clean up
        # and let another process try.
        alarm $timeout;
        # Make sure we"re only receiving local connections
        if ($dotted_quad ne "127.0.0.1") {
            MailScanner::Log::WarnLog("MailGuardian: Error: unexpected connection from %s", $dotted_quad);
            close CLIENT;
            next;
        }
        my @in;
        while (<CLIENT>) {
            # End of normal logging message
            last if /^END$/;
            # MailScanner child telling us to shut down
            ExitLogging if /^EXIT$/;
            chop;
            push @in, $_;
        }
        my $data = join "", @in;
        my $tmp = unpack("u", $data);
        $message = thaw $tmp;

        next unless defined $$message{id};

        # Check to make sure DB connection is still valid
        InitConnection unless $dbh->ping;
        my $sth_mail = $dbh->prepare("INSERT INTO mail_message (id, from_address, from_domain, to_address, to_domain, subject, client_ip, mailscanner_hostname, spam_score, timestamp, token, whitelisted, blacklisted, is_spam, is_rbl_listed, stored, infected, size, mailq_id, is_mcp, mcp_score, date, released, scanned) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)") or MailScanner::Log::WarnLog("MailGuardian: Message Error: %s", $DBI::errstr);
        # Log message
        my $message_id = $ug->create_str();
        my $header_id = $ug->create_str();
        my $report_id = $ug->create_str();
        my $mcp_id = $ug->create_str();
        my $rbl_id = $ug->create_str();
        my $spam_id = $ug->create_str();
        my $isrblspam = 0;
        if ($$message{isrblspam} ne undef) {
            $isrblspam = $$message{isrblspam};
        }
        my $issaspam = 0;
        if ($$message{issaspam} ne undef) {
            $issaspam = $$message{issaspam};
        }
        my $issamcp = 0;
        if ($$message{issamcp} ne undef) {
            $issamcp = $$message{issamcp};
        }
        my $scanmail = 0;
        if ($$message{scanmail} ne undef) {
            $scanmail = $$message{scanmail};
        }
        $sth_mail->execute(
            $message_id,
            $$message{from},
            $$message{from_domain},
            $$message{to},
            $$message{to_domain},
            $$message{subject},
            $$message{clientip},
            $$message{hostname},
            $$message{sascore},
            $$message{timestamp},
            $$message{token},
            $$message{spamwhitelisted},
            $$message{spamblacklisted},
            $issaspam,
            $isrblspam,
            $$message{quarantined},
            $$message{virusinfected},
            $$message{size},
            $$message{id},
            $issamcp,
            $$message{mcpsascore},
            $$message{date},
            0,
            $$message{scanmail}
        );
        
        # Uncomment this row for debugging
        #MailScanner::Log::InfoLog("MailGuardian: $message_id: MailGuardian SQL inserted row");

        # This doesn't work in the event we have no connection by now ?
        if (!$sth_mail) {
            MailScanner::Log::WarnLog("MailGuardian: $$message{id}: MailGuardian SQL Cannot insert row: %s", $sth_mail->errstr);
        } else {
            MailScanner::Log::InfoLog("MailGuardian: $$message{id}: Logged to MailGuardian SQL");
        }

        # Uncomment this row for debugging
        #MailScanner::Log::InfoLog("MailGuardian: $$message{id}: MailGuardian SQL Before storing headers");
        my $sth_headers = $dbh->prepare("INSERT INTO mail_headers (id, contents, message_id) VALUES (?, ?, ?)") or MailScanner::Log::WarnLog("MailGuardian: Message Headers Error: %s", $DBI::errstr);        
        # Log Message Headers
        $sth_headers->execute(
            $header_id,
            $$message{headers},
            $message_id
        );

        # Uncomment this row for debugging
        #MailScanner::Log::InfoLog("MailGuardian: $$message{id}: MailGuardian SQL After storing headers");

        # This doesn't work in the event we have no connection by now ?
        if (!$sth_headers) {
            MailScanner::Log::WarnLog("MailGuardian: $$message{id} Headers: MailGuardian SQL Cannot insert row: %s", $sth_headers->errstr);
        } else {
            MailScanner::Log::InfoLog("MailGuardian: $$message{id} Headers: Logged to MailGuardian SQL");
        }

        my $sth_report = $dbh->prepare("INSERT INTO mail_mailscannerreport (id, contents, message_id) VALUES (?, ?, ?)") or MailScanner::Log::WarnLog("MailGuardian: Message MailScanner Report Error: %s", $DBI::errstr);
        # Log Message MailScanner Report
        $sth_report->execute(
            $report_id,
            $$message{reports},
            $message_id
        );

        # This doesn't work in the event we have no connection by now ?
        if (!$sth_report) {
            MailScanner::Log::WarnLog("MailGuardian: $$message{id} MailScanner Report: MailGuardian SQL Cannot insert row: %s", $sth_report->errstr);
        } else {
            MailScanner::Log::InfoLog("MailGuardian: $$message{id} MailScanner Report: Logged to MailGuardian SQL");
        }

        my $sth_mcp = $dbh->prepare("INSERT INTO mail_mcpreport (id, contents, message_id) VALUES (?, ?, ?)") or MailScanner::Log::WarnLog("MailGuardian: Message MCP Report Error: %s", $DBI::errstr);
        # Log Message MCP Report
        $sth_mcp->execute(
            $mcp_id,
            $$message{mcpreport},
            $message_id
        );

        # This doesn't work in the event we have no connection by now ?
        if (!$sth_mcp) {
            MailScanner::Log::WarnLog("MailGuardian: $$message{id} MCP Report: MailGuardian SQL Cannot insert row: %s", $sth_mcp->errstr);
        } else {
            MailScanner::Log::InfoLog("MailGuardian: $$message{id} MCP Report: Logged to MailGuardian SQL");
        }

        my $sth_rbl = $dbh->prepare("INSERT INTO mail_rblreport (id, contents, message_id) VALUES (?, ?, ?)") or MailScanner::Log::WarnLog("MailGuardian: Message RBL Report Error: %s", $DBI::errstr);
        # Log Message RBL Report
        $sth_rbl->execute(
            $rbl_id,
            $$message{rblspamreport},
            $message_id
        );

        # This doesn't work in the event we have no connection by now ?
        if (!$sth_rbl) {
            MailScanner::Log::WarnLog("MailGuardian: $$message{id} RBL Report: MailGuardian SQL Cannot insert row: %s", $sth_rbl->errstr);
        } else {
            MailScanner::Log::InfoLog("MailGuardian: $$message{id} RBL Report: Logged to MailGuardian SQL");
        }

        my $sth_spam = $dbh->prepare("INSERT INTO mail_spamreport (id, contents, message_id) VALUES (?, ?, ?)") or MailScanner::Log::WarnLog("MailGuardian: Message Spam Report Error: %s", $DBI::errstr);
        # Log Message SPAM Report
        $sth_spam->execute(
            $spam_id,
            $$message{spamreport},
            $message_id
        );

        # This doesn't work in the event we have no connection by now ?
        if (!$sth_spam) {
            MailScanner::Log::WarnLog("MailGuardian: $$message{id} SPAM Report: MailGuardian SQL Cannot insert row: %s", $sth_spam->errstr);
        } else {
            MailScanner::Log::InfoLog("MailGuardian: $$message{id} SPAM Report: Logged to MailGuardian SQL");
        }

        #$dbh->commit();

        # Unset
        $message = undef;
        #$message_id = undef;

    }
}

sub EndMailGuardianLogging {
    # Tell server to shut down.  Another child will start a new server
    # if we are here due to old age instead of administrative intervention
    socket(TO_SERVER, PF_INET, SOCK_STREAM, getprotobyname("tcp"));
    my $addr = sockaddr_in($server_port, $loop);
    connect(TO_SERVER, $addr) or return;

    print TO_SERVER "EXIT\n";
    close TO_SERVER;
}

sub MailGuardianLogging {
    my ($message) = @_;

    # Don't bother trying to do an insert if no message is passed-in
    return unless $message;

    #Uncomment below lines for debugging
    #my $msgid = $message->{id};
    #if (open(MESSAGE, "> /tmp/msg-$msgid")) {
    #    MailScanner::Log::InfoLog(MESSAGE Dumper($message));
    #    close(MESSAGE);
    #}

    # Fix duplicate 'to' addresses for Postfix users
    my (%rcpts);
    map { $rcpts{$_} = 1; } @{$message->{to}};
    @{$message->{to}} = keys %rcpts;

    # Get rid of control chars and fix chars set in Subject
    my $subject = fix_latin($message->{utf8subject});
    $subject =~ s/\n/ /g;  # Make sure text subject only contains 1 line (LF)
    $subject =~ s/\t/ /g;  # and no TAB characters
    $subject =~ s/\r/ /g;  # and no CR characters

    # Uncommet the folloging line when debugging SQLBlackWhiteList.pm
    #MailScanner::Log::WarnLog("MailGuardian: Debug: var subject: %s", Dumper($subject));

    # Get rid of control chars and tidy-up SpamAssassin report
    my $spamreport = $message->{spamreport};
    $spamreport =~ s/\n/ /g;  # Make sure text report only contains 1 line (LF)
    $spamreport =~ s/\t//g;   # and no TAB characters
    $spamreport =~ s/\r/ /g;  # and no CR characters

    # Get rid of control chars and tidy-up SpamAssassin MCP report
    my $mcpreport = $message->{mcpreport};
    $mcpreport =~ s/\n/ /g;  # Make sure text report only contains 1 line (LF)
    $mcpreport =~ s/\t//g;   # and no TAB characters
    $mcpreport =~ s/\r/ /g;  # and no CR characters

    # Workaround tiny bug in original MCP code
    my ($mcpsascore);
    if (defined $message->{mcpsascore}) {
        $mcpsascore = $message->{mcpsascore};
    } else {
        $mcpsascore = $message->{mcpscore};
    }

    # Set quarantine flag - This only works on MailScanner 4.43.7 or later
    my ($quarantined);
    $quarantined = 0;
    if ((scalar(@{$message->{quarantineplaces}}))
        + (scalar(@{$message->{spamarchive}})) > 0)
    {
        $quarantined = 1;
    }

    # Get timestamp, and format it so it is suitable to use with PostgreSQL
    my ($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime();
    my ($timestamp) = sprintf("%d-%02d-%02d %02d:%02d:%02d",
        $year + 1900, $mon + 1, $mday, $hour, $min, $sec);

    my ($date) = sprintf("%d-%02d-%02d", $year + 1900, $mon + 1, $mday);
    my ($time) = sprintf("%02d:%02d:%02d", $hour, $min, $sec);

    # Also print 1 line for each report about this message. These lines
    # contain all the info above, + the attachment filename and text of
    # each report.
    my ($file, $text, @report_array);
    while(($file, $text) = each %{$message->{allreports}}) {
        $file = "the entire message" if $file eq "";
        # Use the sanitised filename to avoid problems caused by people forcing
        # logging of attachment filenames which contain nasty SQL instructions.
        $file = $message->{file2safefile}{$file} or $file;
        $text =~ s/\n/ /g;  # Make sure text report only contains 1 line (LF)
        $text =~ s/\t/ /g;  # and no TAB characters
        $text =~ s/\r/ /g;  # and no CR characters

        # Uncommet the folloging line when debugging MailGuardian.pm
        #MailScanner::Log::WarnLog("MailGuardian: Debug: VAR text: %s", Dumper($text));

        push (@report_array, $text);
    }

    # Sanitize reports
    my $reports = join(",", @report_array);

    # Uncommet the folloging line when debugging MailGuardian.pm
    #MailScanner::Log::WarnLog("MailGuardian: DEBUG: var reports: %s", Dumper($reports));

    # Fix the $message->{clientip} for later versions of Exim
    # where $message->{clientip} contains ip.ip.ip.ip.port
    my $clientip = $message->{clientip};
    $clientip =~ s/^(\d+\.\d+\.\d+\.\d+)(\.\d+)$/$1/;

    # Integrate SpamAssassin Whitelist/Blacklist reporting
    if ($spamreport =~ /USER_IN_WHITELIST/) {
        $message->{spamwhitelisted} = 1;
    }
    if ($spamreport =~ /USER_IN_BLACKLIST/) {
        $message->{spamblacklisted} = 1;
    }

    # Get the first domain from the list of recipients
    my ($todomain, @todomain);
    @todomain = @{$message->{todomain}};
    $todomain = $todomain[0];
    
    # Generate token for mail viewing
    my ($token, $sha1);
    $sha1 = Digest::SHA1->new;
    $sha1->add($message->{id}, $timestamp, $message->{size}, $message->{headers});
    $token = $sha1->hexdigest;
    
    # Place all data into %msg
    my %msg;
    $msg{timestamp} = $timestamp;
    $msg{id} = $message->{id};
    $msg{size} = $message->{size};
    $msg{from} = $message->{from};
    $msg{from_domain} = $message->{fromdomain};
    $msg{to} = join(",", @{$message->{to}});
    $msg{to_domain} = $todomain;
    $msg{subject} = $subject;
    $msg{clientip} = $clientip;
    $msg{archiveplaces} = join(",", @{$message->{archiveplaces}});
    $msg{isspam} = $message->{isspam};
    $msg{ishigh} = $message->{ishigh};
    $msg{issaspam} = $message->{issaspam};
    $msg{isrblspam} = $message->{isrblspam};
    $msg{spamwhitelisted} = $message->{spamwhitelisted};
    $msg{spamblacklisted} = $message->{spamblacklisted};
    $msg{sascore} = $message->{sascore};
    $msg{spamreport} = $spamreport;
    $msg{ismcp} = $message->{ismcp};
    $msg{ishighmcp} = $message->{ishighmcp};
    $msg{issamcp} = $message->{issamcp};
    $msg{mcpwhitelisted} = $message->{mcpwhitelisted};
    $msg{mcpblacklisted} = $message->{mcpblacklisted};
    $msg{mcpsascore} = $mcpsascore;
    $msg{mcpreport} = $mcpreport;
    $msg{virusinfected} = $message->{virusinfected};
    $msg{nameinfected} = $message->{nameinfected};
    $msg{otherinfected} = $message->{otherinfected};
    $msg{reports} = $reports;
    $msg{hostname} = $hostname;
    $msg{date} = $date;
    $msg{"time"} = $time;
    $msg{headers} = join("\n", map { fix_latin($_)} @{$message->{headers}});
    $msg{quarantined} = $quarantined;
    $msg{rblspamreport} = $message->{rblspamreport};
    $msg{token} = $token;

    # Prepare data for transmission
    my $f = freeze \%msg;
    my $p = pack("u", $f);

    # Connect to server
    while (1) {
        socket(TO_SERVER, PF_INET, SOCK_STREAM, getprotobyname("tcp"));
        my $addr = sockaddr_in($server_port, $loop);
        connect(TO_SERVER, $addr) and last;
        # Failed to connect - kick off new child, wait, and try again
        InitMailGuardianLogging();
        sleep 5;
    }

    # Pass data to server process
    MailScanner::Log::InfoLog("MailGuardian: Logging message $msg{id} to SQL");
    print TO_SERVER $p;
    print TO_SERVER "END\n";
    close TO_SERVER;
}

1;