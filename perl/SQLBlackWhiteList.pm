#
# MailGuardian for MailScanner
# Copyright (C) 2003-2011  Steve Freegard (steve@freegard.name)
# Copyright (C) 2011  Garrod Alwood (garrod.alwood@lorodoes.com)
# Copyright (C) 2014-2017  MailWatch Team (https://github.com/MailWatch/1.2.0/graphs/contributors)
# Copyright (C) 2018 @KHIT93 (https://github.com/khit93/mailguardian/contributers.md)
#
#   Custom Module SQLBlackWhiteList
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

use strict 'vars';
use strict 'refs';
no  strict 'subs'; # Allow bare words for parameter %'s

use vars qw($VERSION);

# Uncommet the folloging line when debugging SQLBlackWhiteList.pm
#use Data::Dumper;

### The package version, both in 1.23 style *and* usable by MakeMaker:
$VERSION = substr q$Revision: 1.0 $, 10;

use DBI;
my (%Whitelist, %Blacklist);
my ($wtime, $btime);
my ($dbh);
my ($sth);

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

#
# Initialise SQL spam whitelist and blacklist
#
sub InitSQLWhitelist {
    MailScanner::Log::InfoLog("MailGuardian: Starting up MailGuardian SQL Whitelist");
    my $entries = CreateList('whitelisted', \%Whitelist);
    MailScanner::Log::InfoLog("MailGuardian: Read %d whitelist entries", $entries);
    $wtime = time();
}

sub InitSQLBlacklist {
    MailScanner::Log::InfoLog("MailGuardian: Starting up MailGuardian SQL Blacklist");
    my $entries = CreateList('blacklisted', \%Blacklist);
    MailScanner::Log::InfoLog("MailGuardian: Read %d blacklist entries", $entries);
    $btime = time();
}

#
# Lookup a message in the by-domain whitelist and blacklist
#
sub SQLWhitelist {
    # Do we need to refresh the data?
    if ((time() - $wtime) >= ($bwl_refresh_time * 60)) {
        MailScanner::Log::InfoLog("MailGuardian: Whitelist refresh time reached");
        InitSQLWhitelist();
    }
    my ($message) = @_;
    return LookupList($message, \%Whitelist);
}

sub SQLBlacklist {
    # Do we need to refresh the data?
    if ((time() - $btime) >= ($bwl_refresh_time * 60)) {
        MailScanner::Log::InfoLog("MailGuardian: Blacklist refresh time reached");
        InitSQLBlacklist();
    }
    my ($message) = @_;
    return LookupList($message, \%Blacklist);
}

#
# Close down the SQL whitelist and blacklist
#
sub EndSQLWhitelist {
    MailScanner::Log::InfoLog("MailGuardian: Closing down MailGuardian SQL Whitelist");
}

sub EndSQLBlacklist {
    MailScanner::Log::InfoLog("MailGuardian: Closing down MailGuardian SQL Blacklist");
}

sub CreateList {
    my ($type, $BlackWhite) = @_;
    my ($sql, $to_address, $from_address, $count, $filter);

    $dbh = DBI->connect("DBI:Pg:database=$db_name;host=$db_host",
        $db_user, $db_pass,
        { PrintError => 0, AutoCommit => 1, RaiseError => 1}
    );
    if (!$dbh) {
        MailScanner::Log::WarnLog("MailGuardian: SQLBlackWhiteList::CreateList::: Unable to initialise database connection: %s", $DBI::errstr);
    }

    # Uncommet the folloging line when debugging SQLBlackWhiteList.pm
    #MailScanner::Log::WarnLog("MailGuardian: DEBUG SQLBlackWhiteList: CreateList: %s", Dumper($BlackWhite));
    
    # Remove old entries
    for (keys %$BlackWhite) {
        delete $BlackWhite->{$_};
    }
    
    $sql = "SELECT to_address, from_address FROM list_entries WHERE listing_type=$type";
    $sth = $dbh->prepare($sql);
    $sth->execute;
    $sth->bind_columns(undef, \$to_address, \$from_address);
    $count = 0;
    
    while($sth->fetch()) {
        $BlackWhite->{lc($to_address)}{lc($from_address)} = 1; # Store entry
        $count++;
    }
    # Uncommet the folloging line when debugging SQLBlackWhiteList.pm
    #MailScanner::Log::WarnLog("MailGuardian: DEBUG SQLBlackWhiteList: CreateList: %s", Dumper($BlackWhite));
    
    # Close connections
    $sth->finish();
    $dbh->disconnect();

    return $count;
}

#
# Based on the address it is going to, choose the right spam white/blacklist.
# Return 1 if the "from" address is white/blacklisted, 0 if not.
#
sub LookupList {
    my ($message, $BlackWhite) = @_;

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
        return 1 if $BlackWhite->{$i}{$from};
        return 1 if $BlackWhite->{$i}{$fromdomain};
        return 1 if $BlackWhite->{$i}{'@'.$fromdomain};
        return 1 if $BlackWhite->{$i}{$ip};
        return 1 if $BlackWhite->{$i}{$ip3};
        return 1 if $BlackWhite->{$i}{$ip3c};
        return 1 if $BlackWhite->{$i}{$ip2};
        return 1 if $BlackWhite->{$i}{$ip2c};
        return 1 if $BlackWhite->{$i}{$ip1};
        return 1 if $BlackWhite->{$i}{$ip1c};
        return 1 if $BlackWhite->{$i}{'*'};
        foreach (@subdomains) {
            return 1 if $BlackWhite->{$i}{$_};
        }
    }

    # It is not in the list
    return 0;
}

1;