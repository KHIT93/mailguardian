#
# MailGuardian
# Copyright (C) 2003-2011  Steve Freegard (steve@freegard.name)
# Copyright (C) 2011  Garrod Alwood (garrod.alwood@lorodoes.com)
# Copyright (C) 2014-2017  MailWatch Team (https://github.com/MailWatch/1.2.0/graphs/contributors)
# Copyright (C) 2018 @KHIT93 (https://github.com/khit93/mailguardian/contributers.md)
#
#   Custom Module SQLBlockAllowList
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

use strict 'vars';
use strict 'refs';
no  strict 'subs'; # Allow bare words for parameter %'s

use vars qw($VERSION);

# Uncommet the folloging line when debugging SQLAllowBlockList.pm
#use Data::Dumper;

### The package version, both in 1.23 style *and* usable by MakeMaker:
$VERSION = '3.0.0';

use DBI;
my (%Allowlist, %Blocklist);
my ($wtime, $btime);
my ($dbh);
my ($sth);
my ($SQLversion);

# Get database information from MailGuardianConf.pm
use File::Basename;
my $dirname = dirname(__FILE__);
require $dirname.'/MailGuardianConf.pm';

my ($db_name) = MailGuardian_get_db_name();
my ($db_host) = MailGuardian_get_db_host();
my ($db_user) = MailGuardian_get_db_user();
my ($db_pass) = MailGuardian_get_db_password();

# Get refresh time from from MailGuardianConf.pm
my ($bwl_refresh_time) =  MailGuardian_get_BWL_refresh_time();

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

#
# Initialise SQL spam allowlist and blocklist
#
sub InitSQLAllowlist {
    MailScanner::Log::InfoLog("MailGuardian: Starting up MailGuardian SQL Allowlist");
    my $entries = CreateList('allowed', \%Allowlist);
    MailScanner::Log::InfoLog("MailGuardian: Read %d allowlist entries", $entries);
    $wtime = time();
}

sub InitSQLBlocklist {
    MailScanner::Log::InfoLog("MailGuardian: Starting up MailGuardian SQL Blocklist");
    my $entries = CreateList('blocked', \%Blocklist);
    MailScanner::Log::InfoLog("MailGuardian: Read %d blocklist entries", $entries);
    $btime = time();
}

#
# Lookup a message in the by-domain allowlist and blocklist
#
sub SQLAllowlist {
    # Do we need to refresh the data?
    if ((time() - $wtime) >= ($bwl_refresh_time * 60)) {
        MailScanner::Log::InfoLog("MailGuardian: Allowlist refresh time reached");
        InitSQLAllowlist();
    }
    my ($message) = @_;
    return LookupList($message, \%Allowlist);
}

sub SQLBlocklist {
    # Do we need to refresh the data?
    if ((time() - $btime) >= ($bwl_refresh_time * 60)) {
        MailScanner::Log::InfoLog("MailGuardian: Blocklist refresh time reached");
        InitSQLBlocklist();
    }
    my ($message) = @_;
    return LookupList($message, \%Blocklist);
}

#
# Close down the SQL allowlist and blocklist
#
sub EndSQLAllowlist {
    MailScanner::Log::InfoLog("MailGuardian: Closing down MailGuardian SQL Allowlist");
}

sub EndSQLBlocklist {
    MailScanner::Log::InfoLog("MailGuardian: Closing down MailGuardian SQL Blocklist");
}

sub CreateList {
    my ($type, $BlockAllow) = @_;
    my ($sql, $to_address, $from_address, $count, $filter);

    my $version = CheckSQLVersion();

    # Database connection failed, so return 0 (count) and exit early
    if ($version == 1) {
        return 0;
    }

    eval {
        $dbh = DBI->connect("DBI:Pg:database=$db_name;host=$db_host",
            $db_user, $db_pass,
            { PrintError => 0, AutoCommit => 1, RaiseError => 1}
        );
    };
    if ($@ || !$dbh) {
        MailScanner::Log::WarnLog("MailGuardian: SQLBlockAllowList::CreateList::: Unable to initialise database connection: %s", $DBI::errstr);
        return 0;
    }

    # Uncommet the folloging line when debugging SQLBlockAllowList.pm
    #MailScanner::Log::WarnLog("MailGuardian: DEBUG SQLBlockAllowList: CreateList: %s", Dumper($BlockAllow));
    
    # Remove old entries
    for (keys %$BlockAllow) {
        delete $BlockAllow->{$_};
    }
    
    $sql = "SELECT to_address, from_address FROM list_entries WHERE listing_type='$type'";
    $sth = $dbh->prepare($sql);
    $sth->execute;
    $sth->bind_columns(undef, \$to_address, \$from_address);
    $count = 0;
    
    while($sth->fetch()) {
        $BlockAllow->{lc($to_address)}{lc($from_address)} = 1; # Store entry
        $count++;
    }

    # TODO: Find out what this code is used for in MailWatch and see if we need something similar
    # $sql = "SELECT filter, from_address FROM $type INNER JOIN user_filters ON $type.to_address = user_filters.username";
    # $sth = $dbh->prepare($sql);
    # $sth->execute;
    # $sth->bind_columns(undef, \$filter, \$from_address);
    # while($sth->fetch()) {
    #     $BlackWhite->{lc($filter)}{lc($from_address)} = 1; # Store entry
    #     $count++;
    # }

    # Uncommet the folloging line when debugging SQLBlockAllowList.pm
    #MailScanner::Log::WarnLog("MailGuardian: DEBUG SQLBlockAllowList: CreateList: %s", Dumper($BlockAllow));
    
    # Close connections
    $sth->finish();
    $dbh->disconnect();

    return $count;
}

#
# Based on the address it is going to, choose the right spam allow/blocklist.
# Return 1 if the "from" address is allowed/blocked, 0 if not.
#
sub LookupList {
    my ($message, $BlockAllow) = @_;

    return 0 unless $message; # Sanity check the input

    # Find the "from" address and the first "to" address
    my ($from, $fromdomain, $toAdd, $todomainAdd, @todomain, $todomain, @to, $to, $ip, $ip1, $ip1c, $ip2, $ip2c, $ip3, $ip3c, $subdom, $i, @keys, @subdomains);
    $from = $message->{from};
    $fromdomain = $message->{fromdomain};
    # Create a array of subdomains for subdomain and tld wildcard matching
    #   e.g. me@this.that.example.com generates subdomain/tld list of ('that.example.com', 'example.com', 'com')
    $subdom = $fromdomain;
    @subdomains = ();
    while ($subdom =~ /.*?\.(.*)/) {
        $subdom = $1;
        push (@subdomains, "*.".$subdom);
    }

    @keys = ('*');
    @todomain = @{$message->{todomain}};
    @to = @{$message->{to}};
    foreach $toAdd (@to) {
        push (@keys, $toAdd);
    }
    foreach $todomainAdd (@todomain) {
        push (@keys, $todomainAdd);
    }
    $ip = $message->{clientip};
    
    # Match on leading 3, 2, or 1 octets
    $ip =~ /(\d{1,3}\.)(\d{1,3}\.)(\d{1,3}\.)/;  # get 1st three octets of IP
    $ip3 = "$1$2$3";
    $ip3c = substr($ip3, 0, - 1);
    $ip2 = "$1$2";
    $ip2c = substr($ip2, 0, - 1);
    $ip1 = $1;
    $ip1c = substr($ip1, 0, - 1);

    # $ip1, $ip2, $ip3 all end in a trailing "."

    # It is in the list if either the exact address is listed,
    # the domain is listed,
    # the IP address is listed,
    # the first 3, 2, or 1 octets of the ipaddress are listed with or without a trailing dot
    # or a subdomain match of the form *.subdomain.example.com is listed
    foreach (@keys) {
        $i = $_;
        return 1 if $BlockAllow->{$i}{$from};
        return 1 if $BlockAllow->{$i}{$fromdomain};
        return 1 if $BlockAllow->{$i}{'@'.$fromdomain};
        return 1 if $BlockAllow->{$i}{$ip};
        return 1 if $BlockAllow->{$i}{$ip3};
        return 1 if $BlockAllow->{$i}{$ip3c};
        return 1 if $BlockAllow->{$i}{$ip2};
        return 1 if $BlockAllow->{$i}{$ip2c};
        return 1 if $BlockAllow->{$i}{$ip1};
        return 1 if $BlockAllow->{$i}{$ip1c};
        return 1 if $BlockAllow->{$i}{'*'};
        foreach (@subdomains) {
            return 1 if $BlockAllow->{$i}{$_};
        }
    }

    # It is not in the list
    return 0;
}

1;