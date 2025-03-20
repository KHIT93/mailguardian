# Preparations

Before we start, there are a few things that need to be performed to ensure that we are able to properly run MailGuardian on a specific setup

First, it is important to know that while MailGuardian will run in basically any system, that can run MailScanner. the required Perl libraries, PostgreSQL and Python 3.10+.
The list of usable combinations is endless and we can only test some of them. We will therefore provide instructions for the following systems and versions:
- Ubuntu 22.04
- Ubuntu 24.04
- Debian 12
- AlmaLinux 9

The steps for AlmaLinux 9, will most likely also work for RedHat Enterprise Linux, but some of the packages might require you to enable extra repositories

All steps in this documentation asume that you have `sudo` installed and that you have access to a user with `sudo` privileges.
You can also use `root` directly and would simply need to omit the `sudo` command from all examples.

## Creating a working directory
While this step is very optional, we think that it makes it more simple to start at a single point and then work our way outwards from there.

Therefore, we start by creating a folder for holding all the files we need run the following commands:

```bash
sudo mkdir -p /opt/mginstaller
sudo chown $USER: /opt/mginstaller
```

The above creates our working directory at `/opt/mginstaller` and changes the ownership to be our current user. This makes it easier for us to run some of later commands

## Downloading MailScanner
Next we need to download the setup files for MailScanner itself. The easiest is to go to the [Releases](https://github.com/MailScanner/v5/releases) of MailScanner and download the latest version.
At the time of writing this document, the latest version is `5.5.3-2` and you can download it using the command matching your operating system below

Ubuntu/Debian:

```bash
cd /opt/mginstaller
wget https://github.com/MailScanner/v5/releases/download/5.5.3-2/MailScanner-5.5.3-2.noarch.deb
```

AlmaLinux:

```bash
cd /opt/mginstaller
wget https://github.com/MailScanner/v5/releases/download/5.5.3-2/MailScanner-5.5.3-2.rhel.noarch.rpm
```

## Installing required software
The list of required software will depend on the specific configuration to use and if you will be running more than one server a multi-node setup.

The MailGuardian application can be configured in one of the following modes:
- AIO
- Manager
- Worker

The `AIO` mode is the most simple as it will run all the components on the same server. The other modes are covered separately.

Ubuntu/Debian:

```bash
sudo apt update
sudo apt install build-essential python3 python3-dev python3-pip python3-virtualenv python3-poetry wget ca-certificates openssl libpng-dev lsb-release sudo -y
```

AlmaLinux:

```bash
sudo dnf config-manager --set-enabled crb
sudo dnf groupinstall "Development Tools" -y
sudo dnf install epel-release -y
sudo dnf install python3.12 python3.12-devel python3.12-pip python3.12-setuptools python3-virtualenv openssl ca-certificates libpng-devel redhat-lsb-core wget sudo -y
```

## Installing the database server
While the easiest would be to force all installs to use a specific version of the PostgreSQL database server, we have chosen to stick the official OS repositories as much as possible.
We have learned that doing so will make it easier for the sysadmin to perform OS upgrades in the future.

Debian/Ubuntu:

```bash
sudo apt update
sudo apt install postgresql postgresql-server-dev-all libpq-dev
```

AlmaLinux:

```bash
sudo dnf install postgresql postgresql-server libpq-devel
```

## Install an MTA
While technically any MTA supported by MailScanner will work, you will need to find your own way to use the configuration from the MailGuardian database in your MTA.
As a good starting point, we will use `postfix` alongside an extension for connecting to a PostgreSQL database.

For all supported systems, simply install `postfix` and `postfix-pgsql` and you are done

## Installing a webserver
Since MailGuardian is running as an application on the local server, we need a way to expose it to the world. There are many ways, but the most common is to install a webserver.
Then configure the webserver to interact with MailGuardian and we are done.
There are again many webservers and you can choose whichever you want.
We are most familiar with `nginx`, so this is what we will use and you can install it within any of the supported Linux distributions.

## Installing MailScanner
First install the package to your system
Debian/Ubuntu:

```bash
cd /opt/mginstaller
sudo dpkg -i MailScanner-5.5.3-2.noarch.deb
sudo apt install -fy
```

AlmaLinux:

```bash
cd /opt/mginstaller
sudo dnf install MailScanner-5.5.3-2.rhel.noarch.rpm
```

Next we need to run some post-install tasks and the easiest is to simple run this:

```bash
sudo /usr/sbin/ms-configure
```

This will ask a lot of questions. If you want to just run a command and have it complete without asking questions, then this should do the trick:

Debian/Ubuntu:

```bash
sudo /usr/sbin/ms-configure --MTA=none --installClamav=Y --installCPAN=Y --installUnrar=Y --ramdiskSize=0
```

AlmaLinux:
```bash
sudo /usr/sbin/ms-configure --MTA=none --installEPEL=Y --installClamav=Y --configClamav=Y --installTNEF=Y --installUnrar=Y --installidn=Y --SELPermissive=Y --installCPAN=Y --ignoreDeps=Y --ramdiskSize=0
```

## Configure MailScanner for basic operation
This next section will handle some basic configuration tasks using the defaults from the [MailScanner Docs](https://www.mailscanner.info/postfix/).

In `/etc/postfix/main.cf`, make the following changes

```
# MailScanner milter
smtpd_milters = inet:127.0.0.1:33333
# MailScanner milter may use QMQP for delivery
qmqpd_authorized_clients = 127.0.0.1
```

Next, we need to make a lot of changes to `/etc/MailScanner/MailScanner.conf`. Please note that most of these options might already be there. In case an option is already there, simply update the value to macth

```
Run As User = postfix
Run As Group = postfix
Incoming Queue Dir = /var/spool/MailScanner/milterin
Outgoing Queue Dir = /var/spool/MailScanner/milterout
MTA = msmail
MSMail Queue Type = short
Milter Scanner = yes
Milter Dispatcher = postfork
# For QMQP delivery
MSMail Delivery Method = QMQP
MSMail Socket Type = inet
MSMail Relay Port = 628
Milter Ignore Loopback = no
```

Next adjust permissions:

```bash
sudo chown postfix:postfix /var/spool/MailScanner/milterin
sudo chown postfix:postfix /var/spool/MailScanner/milterout
```

The official docs want you to start the services at this point. Unless you want to do a smoketest, there is no point it doing it at this point, since we will make more changes

## Install and configure MailGuardian
The next steps, we will asume some default values. DO NOT see these as secure, but instead as easy to understand examples.

PostgreSQL User = mailguardian
PostgreSQL Password = M@ilGuard1an
PostgreSQL Database = mailguardian



## Configure the PostgreSQL database
TBD

### Install the application
TBD

### Configuration changes for MailScanner
Here we need to make some changes to `/etc/MailScanner/MailScanner.conf`. Please note that most of these options might already be there. In case an option is already there, simply update the value to macth

```
Always Looked Up Last = &MailGuardianLogging
Detailed Spam Report = yes
Quarantine Whole Message = yes
Quarantine Whole Messages As Queue Files = no
Include Scores In SpamAssassin Report = yes
Incoming Work User = postfix
Incoming Work Group = postfix
Incoming Work Permissions = 0660
Quarantine User = postfix
Quarantine Group = postfix
Quarantine Permissions = 0644
Is Definitely Not Spam = &SQLAllowlist
Is Definitely Spam = &SQLBlocklist
Spam Actions = store header "X-Spam-Status:Yes"
Non Spam Actions = store deliver header "X-Spam-Status:No"
Log Spam = yes
Log Silent Viruses = yes
Log Dangerous HTML Tags = yes
Use SpamAssassin = &SQLNoScan
Definite Spam Is High Scoring = yes
Required SpamAssassin Score = &SQLSpamScores
High SpamAssassin Score = &SQLHighSpamScores
```

### Configure SpamAssassin
Next we need to make some changes to how SpamAssassin works, so that we can shared the state of what is spam and what is not

Make the following changes to `/etc/MailScanner/spamassassin.conf`. Please note that most of these options might already be there. In case an option is already there, simply update the value to macth

```
bayes_path /etc/MailScanner/bayes/bayes
bayes_file_mode 0660
bayes_store_module Mail::SpamAssassin::BayesStore::PgSQL
bayes_sql_dsn DBI:Pg:mailguardian:localhost:5432
bayes_sql_username mailguardian
bayes_sql_password M@ilGuard1an
```

### Configure Postfix
Next we need to make some changes to Postfix, so that MailGuardian can manage what we will process

Make the following changes to `/etc/postfix/main.cf`. Please note that most of these options might already be there. In case an option is already there, simply update the value to macth

```
relay_domains = proxy:pgsql:/etc/postfix/pgsql-transport.cf
transport_maps = proxy:pgsql:/etc/postfix/pgsql-transport.cf
```

Find the line for `mynetworks`and append the following value to it:

```
, proxy:pgsql:/etc/postfix/pgsql-mynetworks.cf
```

Next create `/etc/postfix/pgsql-transport.cf`

```
user = mailguardian
password = M@ilGuard1an
hosts = localhost
dbname = mailguardian
query = SELECT CONCAT(relay_type,':[',destination,']') from domains where name='%s' AND active = '1';
```

Next create `/etc/postfix/pgsql-mynetworks.cf`

```
user = mailguardian
password = M@ilGuard1an
hosts = localhost
dbname = mailguardian
query = SELECT ip_address from smtp_relays where (ip_address='%s' or hostname='%s') AND active = '1';
```