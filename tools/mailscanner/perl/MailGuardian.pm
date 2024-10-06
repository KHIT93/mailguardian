#
# MailGuardian
# Copyright (C) 2003-2011  Steve Freegard (steve@freegard.name)
# Copyright (C) 2011  Garrod Alwood (garrod.alwood@lorodoes.com)
# Copyright (C) 2014-2017  MailWatch Team (https://github.com/MailWatch/1.2.0/graphs/contributors)
# Copyright (C) 2018 @KHIT93 (https://github.com/khit93/mailguardian/contributers.md)
#
#   Custom Module MailGuardian
#
#   Version 3.0.0
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
use DBD:Pg;
use JSON;
use utf8;
use Data::UUID;
use Sys::Hostname;
use Storable(qw[freeze thaw]);
use POSIX;
use Socket;
use Encoding::FixLatin qw(fix_latin);
use Digest::SHA1;
use Sys::Syslog;

# Uncommet the following line when debugging MailGuardian.pm
#use Data::Dumper;

use vars qw($VERSION);

### The package version, both in 1.23 style *and* usable by MakeMaker:
$VERSION = '3.0.0';

# Trace settings - uncomment this to debug
#DBI->trace(2,'/tmp/dbitrace.log');

my ($dbh);
my ($sth_mail);
my ($sth_task);
my $current_message_id;

my ($hostname) = hostname;
my $loop = inet_aton("127.0.0.1");
my $server_port = 11553;
my $timeout = 3600;
my $ug = Data::UUID->new;
my ($SQLversion);

# Get database information from MailGuardianConf.pm
use File::Basename;
my $dirname = dirname(__FILE__);
require $dirname.'/MailGuardianConf.pm';

my ($db_name) = MailGuardian_get_db_name();
my ($db_host) = MailGuardian_get_db_host();
my ($db_user) = MailGuardian_get_db_user();
my ($db_pass) = MailGuardian_get_db_password();

my $RunInForeground;

sub InitMailWatchLogging {
    # Detect if MailScanner Milter is calling this custom function and do not spawn
    # MSMilter uses the blocklists and allowlists, but not the logger
    if ($0 !~ /MSMilter/) {
        # Grab values from config prior to fork, after which MailScanner methods become
        # inaccessible to descendant
        my $facility = MailScanner::Config::Value('logfacility');
        my $logsock  = MailScanner::Config::Value('logsock');
        $RunInForeground = MailScanner::Config::Value('runinforeground');

        $| = 1 if $RunInForeground;

        my $pid = fork();
        if ($pid) {
            # MailScanner child process
            waitpid $pid, 0;
        } else {
            # New process
            # Detach from parent, make connections, and listen for requests
            POSIX::setsid();
            if (!fork()) {
                $SIG{HUP} = $SIG{INT} = $SIG{PIPE} = $SIG{TERM} = $SIG{ALRM} = \&ExitLogging;
                alarm $timeout;
                $0 = "MailGuardian SQL";

                # Reinitialize logging (cannot use MailScanner::Log due to detach)
                if ($logsock eq '') {
                    if ($^O =~ /solaris|sunos|irix/i) {
                        $logsock = 'udp';
                    } else {
                        $logsock = 'unix';
                    }
                }

                eval { Sys::Syslog::setlogsock($logsock) unless $RunInForeground; };
                eval { Sys::Syslog::openlog($0, 'pid, nowait', $facility) unless $RunInForeground; };
                
                # Listen for messages unless connection can't be initialized
                ListenForMessages() unless InitConnection() == 1;
            }
        exit;
        }
    }
}

sub CheckSQLVersion {
    # Prevent Logger from dying if connection fails
    eval {
        $dbh = DBI->connect("DBI:Pg:database=$db_name;host=$db_host",
            $db_user, $db_pass,
            { PrintError => 0, AutoCommit => 1, RaiseError => 1 }
        );
    };
    if ($@ || !$dbh) {
        LogMessage("warn", "Unable to initialise database connection: $DBI::errstr");
        close(SERVER);
        return 1;
    }
    $SQLversion = $dbh->{pg_server_version};
    $dbh->disconnect;

    return $SQLversion;
}

sub LogMessage {
    my $level = shift;
    my $msg = shift;

    eval {
        if (!$RunInForeground) {
            Sys::Syslog::syslog($level, $msg);
        } else {
            print STDOUT "$0: $level: $msg\n";
        }
    };
}

sub BindPort {
    # Set up TCP/IP socket.  We will start one server per MailScanner
    # child, but only one child will actually be able to get the socket.
    # The rest will die silently.  When one of the MailScanner children
    # tries to log a message and fails to connect, it will start a new
    # server.
    socket(SERVER, PF_INET, SOCK_STREAM, getprotobyname("tcp"));
    setsockopt(SERVER, SOL_SOCKET, SO_REUSEADDR, 1);
    my $addr = sockaddr_in($server_port, $loop);
    bind(SERVER, $addr) or return 1;

    return 0;
}

sub ListenPort {
    # Start listening
    listen(SERVER, SOMAXCONN) or return 1;

    return 0;
}

sub InitDB {
    # Our reason for existence - the persistent connection to the database
    my $version = CheckSQLVersion();

    if ($version == 1) {
       return 1;
    }

    eval { $dbh = DBI->connect("DBI:Pg:database=$db_name;host=$db_host",
            $db_user, $db_pass,
            { PrintError => 0, AutoCommit => 1, RaiseError => 1 }
        );
    };
    if ($@ || !$dbh) {
        LogMessage('warn', "Unable to initialise database connection: $DBI::errstr");
        return 1;
    }
    $dbh->do('SET NAMES utf8mb4');

    $sth_mail = $dbh->prepare("INSERT INTO messages (id, from_address, from_domain, to_address, to_domain, subject, client_ip, mailscanner_hostname, spam_score, timestamp, token, allowed, blocked, is_spam, is_rbl_listed, stored, infected, size, mailq_id, is_mcp, mcp_score, date, released, scanned) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) RETURNING id");
    if (!$sth_mail) {
        LogMessage('warn', "Error: $DBI::errstr" );
        return 1;
    }
    $sth_task = $dbh->prepare("INSERT INTO tasks (uuid, module, task, payload) VALUES (?, ?, ?, ?)");
    if (!$sth_task) {
        LogMessage('warn', "Error: $DBI::errstr" );
        return 1;
    }

    return 0;
}

sub InitConnection {
    # Fail to bind, we'll just exit, port in use
    if (BindPort() == 1) { return 1; }
    if (InitDB() == 1) {
        # We are bound, but couldn't connect to DB, so close it all down
        close(SERVER);
        return 1;
    }
    if (ListenPort() == 1) {
        # We are bound, connected to DB but can't listen, so close it all down
        close(SERVER);
        return 1;
    }
    return 0;
}

sub ExitLogging {
    # Server exit - commit changes, close socket, and exit gracefully.
    close(SERVER);
    $dbh->disconnect;
    exit;
}

sub ListenForMessages {
    my $message;
    LogMessage('info', "Started MailGuardian SQL Logging child");
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
            LogMessage('warn', "Error: unexpected connection from $dotted_quad");
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

        # Set up a loop to prevent loss of logging, up to $timeout
        # Prevents loss of logging to database due to temporary failure
        while(1) {
            eval {$sth_mail->execute(
                $ug->create_str(), # uuid
                $$message{from}, # from_address
                $$message{from_domain}, # from_domain
                $$message{to}, # to_address
                $$message{to_domain}, # to_domain
                $$message{subject}, # subject
                $$message{clientip}, # client_ip
                $$message{archiveplaces}, # NOT YET IDENTIFIED
                $$message{isspam}, # is_spam
                $$message{ishigh}, # NOT YET IDENTIFIED
                $$message{issaspam}, # NOT YET IDENTIFIED
                $$message{isrblspam}, # is_rbl_listed
                $$message{spamwhitelisted}, # allowed
                $$message{spamblacklisted}, # blocked
                $$message{sascore}, #spam_score
                $$message{spamreport}, # SEPARATE STATEMENT
                $$message{virusinfected}, # NOT YET IDENTIFIED
                $$message{nameinfected}, # NOT YET IDENTIFIED
                $$message{otherinfected}, # NOT YET IDENTIFIED
                $$message{reports}, # SEPARATE STATEMENT
                $$message{ismcp}, # is_mcp
                $$message{ishighmcp}, # NOT YET IDENTIFIED
                $$message{issamcp}, # NOT YET IDENTIFIED
                $$message{mcpwhitelisted}, # NOT YET IDENTIFIED
                $$message{mcpblacklisted}, # NOT YET IDENTIFIED
                $$message{mcpsascore}, # NOT YET IDENTIFIED
                $$message{mcpreport}, # SEPARATE STATEMENT
                $$message{hostname}, # mailscanner_hostname
                $$message{date}, # date
                $$message{"time"}, # NOT YET IDENTIFIED
                $$message{headers}, # SEPARATE STATEMENT
                $$message{quarantined}, # stored
                $$message{rblspamreport}, # SEPARATE STATEMENT
                $$message{token}, # NOT YET IDENTIFIED
                $$message{messageid} # mail_message_id
            );};

            $current_message_id = $sth_mail->fetchrow_array();

            my %headers_payload = ('message_id'=>$current_message_id, 'headers'=>$$message{headers})
            my %spamreport_payload = ('message_id'=>$current_message_id, 'spamreport'=>$$message{spamreport})

            eval {$sth_task->execute(
                $ug->create_str(), # uuid
                'mailguardian.app.tasks.message_headers', # module
                'message_headers_to_db', # task
                encode_json \%headers_payload # payload
            )}

            eval {$sth_task->execute(
                $ug->create_str(), # uuid
                'mailguardian.app.tasks', # module
                'spamassassin_report_to_db', # task
                encode_json \%spamreport_payload # payload
            )}

            # Something went wrong
            if ($@ || !$sth_mail) {
                LogMessage('warn', "$$message{id}: Cannot insert row: $sth_mail->errstr");
                close(SERVER);
                # Bind the port so another instance can't spawn
                if (BindPort() == 1) {
                    # Can't bind, unexpected, bail out
                    last;
                }
                while(InitDB() == 1) { sleep(2); };
                # Start listening once all is well
                if (ListenPort() == 1) {
                    # Can't listen, unexpected, bail out
                    last;
                }
            } else {
                LogMessage('info', "$$message{id}: Logged to MailGuardian SQL");
                last;
            }
        }


sub EndMailWatchLogging {
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

    # Fix duplicate 'to' addresses for Postfix users
    my (%rcpts);
    map { $rcpts{$_} = 1; } @{$message->{to}};
    @{$message->{to}} = keys %rcpts;

    # Get rid of control chars and fix chars set in Subject
    my $subject = fix_latin($message->{utf8subject});
    $subject =~ s/\n/ /g;  # Make sure text subject only contains 1 line (LF)
    $subject =~ s/\t/ /g;  # and no TAB characters
    $subject =~ s/\r/ /g;  # and no CR characters

    # Uncommet the following line when debugging SQLBlockAllowList.pm
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

    # Integrate SpamAssassin Allowlist/Blocklist reporting
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

    # Extract message id from header
    my ($messageid, $inmessageid, $messageidbuffer);
    $messageid = "";
    $messageidbuffer = "";
    $inmessageid = 0;

    # Extract message id from header (unfold header if needed)
    foreach (@{$message->{headers}}) {
        if ( $_ =~ /^message-id:\s/i ) {
            # RFC 822 unfold message-id
            $messageidbuffer = $_;
            $inmessageid = 1;
            next;
        } elsif ($inmessageid) {
            if ($_ =~ /^\s/) {
                # In continuation line
                $messageidbuffer .= $_;
            } else {
                # End of message-id field
                last;
            }
        }
    }

    # Set the re-formatted message-id and trim it
    ($messageid = $messageidbuffer) =~ s/^message-id:\s+//i;
    $messageid =~ s/^\s+|\s+$//g;

    # Warn if Message-ID was not found
    if ($messageid eq "") {
      MailScanner::Log::WarnLog("MailGuardian: Could not extract Message-ID for %s", $message->{id});
    }
    
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
    $msg{spamreport} = fix_latin($spamreport);
    $msg{ismcp} = $message->{ismcp};
    $msg{ishighmcp} = $message->{ishighmcp};
    $msg{issamcp} = $message->{issamcp};
    $msg{mcpwhitelisted} = $message->{mcpwhitelisted};
    $msg{mcpblacklisted} = $message->{mcpblacklisted};
    $msg{mcpsascore} = $mcpsascore;
    $msg{mcpreport} = fix_latin($mcpreport);
    $msg{virusinfected} = $message->{virusinfected};
    $msg{nameinfected} = $message->{nameinfected};
    $msg{otherinfected} = $message->{otherinfected};
    $msg{reports} = fix_latin($reports);
    $msg{hostname} = $hostname;
    $msg{date} = $date;
    $msg{"time"} = $time;
    $msg{headers} = join("\n", map { fix_latin($_)} @{$message->{headers}});
    $msg{quarantined} = $quarantined;
    $msg{rblspamreport} = $message->{rblspamreport};
    $msg{token} = $token;
    $msg{messageid} = fix_latin($messageid);

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