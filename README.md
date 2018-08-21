# MailGuardian
A Django-based RESTful SPA (Single Page Application) web GUI for MailScanner.

MailGuardian is your choice no matter if you need a single instance MailScanner deployment for your internal business email services or if you are a commercial hosting company, looking for a modern, reliable and scalable solution for letting you, your staff and your customers easily manage their spam filter appliance.

## Important notice

This software is still pre-release and much of the below documentation is written before some of the application code is actually ready, so until the actual application is tagged with 1.0.0 stable release, you might have some issues when installing.
Once this is no longer the case, even if stable 1.0.0 is not yet tagged, we will remove this notice

## Features

- Built in modern technology 
- Modern web interface that works great on your computer, phone or tablet
- RESTful API for easy integration with other applications
- Multi-node compatible, to allow running multiple MailScanner appliances with one web interface to manage them all
- Three user levels to easily manage access rights
- Supports limits on accounts per domain to support commercial usage

## Supported browsers

- Internet Explorer 11
- Microsoft Edge 12 or newer
- Mozilla Firefox 21 or newer
- Google Chrome 23 or newer
- Apple Safari 6 or newer for macOS/OSX
- Android 4.4 or newer
- iOS 6.1 or newer

## Requirements

### Hardware

We recommend the following requirements for your hardware, regardless of whether you are running with a physical machine or a virtual machine

- 2 CPU cores
- 4GB of RAM (This will vary greatly based on your database size and how much email that you are processing)
- 20GB of SAS storage or SSD storage

### Software

- Debian 9 `Stretch` or CentOS 7
- Python 3.5 or newer
- Python `virtualenv`
- PostgreSQL 10.x
- Postfix 3.10+ with `pgsql` driver
- Nginx 1.10+ or Apache 2.4+ with `HTTP/2` support
- `sudo` installed and configured on your system
- EPEL repository for CentOS
- Stretch Backports for Debian

### Optional requirements

- NodeJS, if you want to compile the assets from the sourcecode
- DataDumper library for `perl` for debugging (libdata-dumper-simple-perl)

## Getting started

Welcome to the MailGuardian documentation. We are glad that you have chosen our applicatin to manage your MailScanner deployment. We have made it unbelievably easy to deploy and manage your own professional spam filtering appliance.
For this to be as easy as possible, we have made the below instructions for the more technical parts of the deployment, to ensure that most people can follow along and get started.

### Prerequisites

Before we start deployment of MailGuardian, we need to have some software installed on our system. This guide currently provides instructions for Debian 9 `Stretch`, but we will also provide commands for CentOS 7. In the meantime, you can refer to the above requirements for what to install.
All commands asume that you are executing them as `root`

This means that we will be installing the following applications:

- `nginx`
- `postfix-pgsql`
- `openssl`
- `python3`
- `sudo`
- `MailScanner`
- An SSL/TLS certificate stored on the server(s), if you do not choose to request a `LetsEncrypt` certificate during installation

First we install what we can from the official Debian `repositories`:

```
apt install sudo wget postfix-pgsql python3 python3-setuptools libpq-dev nginx ca-certificates openssl libpng-dev
easy_install3 virtualenv pip
```

This will install most of the things that we need. Next we will add the official `PostgreSQL` repo to get the latest version of `PostgreSQL 10`

```
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
apt update
apt dist-upgrade
apt install postgresql-10 postgresql-sever-dev-10 postgresql-client-10
```

Next, we need to install MailScanner. Go to https://www.mailscanner.info/downloads/ and download the package that you need, onto your server.
For Debian, we will run these command to get the current version 5.0.7-3 of `MailScanner` and install it
```
wget https://s3.amazonaws.com/msv5/release/MailScanner-5.0.7-3.deb.tar.gz
tar xvzf MailScanner-5.0.7-3.deb.tar.gz
cd MailScanner-5.0.7-3
chmod +x install.sh
./install.sh
```

The installer will ask you some questions and mostly you can just accept the defaults, unless you know what are doing. The only question where we need to choose something else is during the question where we are asked what `MTA` to use. Here we need to make sure that we choose the number corresponding to `postfix`.

Once the installation has finished, we need to configure the filesystem with the correct permissions, as well as add some folders. We can do this with the following commands:

```
mkdir -p /var/spool/MailScanner/spamassassin/
mkdir /etc/MailScanner/bayes
chown root:mtagroup /etc/MailScanner/bayes
chmod g+rws /etc/MailScanner/bayes
chown -R postfix:mtagroup /var/spool/MailScanner/spamassassin
chown -R postfix:postfix /var/spool/MailScanner/incoming
chown -R postfix:postfix /var/spool/MailScanner/quarantine
chmod -R g+r /var/spool/postfix/{hold,incoming}
```

### Installation of MailGuardian

#### Creating the system user

Next, we will create a user, from which we will run our application

```
adduser mailguardian
```

Follow the onscreen prompt to complete the account creation and set a password.

Next we need to assign the new `mailguardian` user to the `mtagroup`, so that we can read the message queue and perform operations on the queue

```
usermod -a -G mtagroup mailguardian
```

#### Installing CPAN modules

This next step is quite easy, as we need to install some `perl modules` using `CPAN`:

```
cpan -i CPAN
cpan -i Data::Dumper
cpan -i Data::UUID
cpan -i HTTP::Date
cpan -i DBI
cpan -i DBD::Pg
cpan -i Encoding::FixLatin
cpan -i Digest::SHA1
cpan -i Mail::ClamAV
cpan -i Mail::SpamAssassin::Plugin::SPF
cpan -i Mail::SpamAssassin::Plugin::URIDNSBL
cpan -i Mail::SpamAssassin::Plugin::DNSEval
```

#### Downloading the application

Next we need to download the application from https://github.com/KHIT93/mailguardian/releases

You can choose to download the sources and then compile the frontend assets (CSS and JavaScript) yourself, or you can download a prebuilt package, where these things are already done. We will cover installation from the prebuilt package.

Right click the link to the prebuilt package mailguardian-X.Y.Z.tar.gz and copy the link.

Run the following commands to download and extract the application:

```
su - mailguardian
wget https://github.com/KHIT93/mailguardian/releases/download/X.Y.Z/mailguardian-X.Y.Z.tar.gz
tar xvzf mailguardian-X.Y.Z.tar.gz
```

This should now create a new folder called `mailguardian` inside `/home/mailguardian`

#### Creating the Python Virtual Environment

Now that we have downloaded the application, we need to transform the code into a virtual environment for `python` to use, so that any other `python` applications on the system are not affected by the dependencies of this application

```
virtualenv -p python3 /home/mailguardian/mailguardian
```

Once this completes, we need to enter the virtual environment and install the `python packages` that are required for the application to run

```
cd /home/mailguardian/mailguardian
source bin/activate
```

Your prompt should now look something like this:
```
(mailguardian) mailguardian@localhost:~/mailguardian$
```

Now we run `pip install -r requirements.txt` to install the necessary `python` packages and libraries that are required for the application to run.

Next we need to install `WSGI` server to run our application. We do not provide one by default, but all our examples and prebuilt scripts asume that we will use `gunicorn`.

You can install `gunicorn` with `pip install gunicorn`.

#### Initializing the application and configuring your webserver

Now that our virtual environment is configured and ready, we need to run `install.py` so that we can get the webserver configured and prepared the application for first start.
The wizard that we start with `python install.py` will ask a series of questions regarding your server configuration and your usage of SSL/TLS certificates. We do this so that the application is secure by default and to support modern technologies like `HTTP/2`, We do therefore provide a prebuilt `systemd` unit file for running the application as service on your system as well as a `nginx` configuration for connecting the webserver to the `unix socket` provided by `gunicorn`.

First run `deactivate` and the type `exit` to log out of the `mailguardian` account and then as `root` change to `home/mailguardian/mailguardian` and run `source bin/activate` and then run `python install.py` and follow the instructions to complete the initial steps of application deployment. As this generates some files and installs some applications, this process can take some time. As we generate a secure `Diffie–Hellman` key parameters of `4096` bits, this part alone can take up to 45 minutes and is a mandatory step, since we force the application to be secure by default.

During exeuction of `install.py`, we will try to guess the hostname of the application and provide you with a URL. This URL will allow you to access the application from your favorite web browser and run the final steps of the installation.

The last thing that we need to do before we can open our favorite web browser and finish the configuration, is to `reload` the configuration files for `nginx`.

To ensure that our configurations are correct and that all certificate files are stored in the correct locations, we first run `nginx -t` and if no errors show, then we run `systemctl reload nginx`.

That is it. Now you can access the application from your favorite web browser.

#### Configure application cron jobs

`MailGuardian` relies on some scheduled tasks to operate correctly and stay optimized. You can either manually enter these in the `crontab` or you can the application do it for you with `python src/manage.py setup_cron`. The automated method using the `setup_cron` command will try to do it correctly, but might still get it wrong if you have a special configuration or some other software on your server.

First get the full path to your `python` executable in your `virtualenv` by activating it, if not already done using `source bin/activate`, and run `which python`. You should get something like `/home/mailguardian/mailguardian/bin/python`

To add the cron jobs manually you need to enter these lines in `crontab -e`

```
@hourly /home/mailguardian/mailguardian/bin/python /home/mailguardian/mailguardian/src/manage.py runjobs hourly
@daily /home/mailguardian/mailguardian/bin/python /home/mailguardian/mailguardian/src/manage.py runjobs daily
@weekly /home/mailguardian/mailguardian/bin/python /home/mailguardian/mailguardian/src/manage.py runjobs weekly
@monthly /home/mailguardian/mailguardian/bin/python /home/mailguardian/mailguardian/src/manage.py runjobs monthly
```

This will make it run at the system predefined settings for each job. If you wish to customize when the cron jobs are running, please see the section about `Custom cron job timing`.sx

#### Initial setup in the browser

Once the installation script, `install.py`, has completed, it is time to perform the final steps of the setup and create our application administrator account. To perform the final steps and start using the application, please visit the URL given at the end of the installation script.
Once you visit the given URL, you will automatically be redirected to the setup screen.

Complete the setup wizard and then log in to the application.

As you will not be able to process any mail without valid domains, you need to go to the `Domains` menu item and create your first domain.

That's it. Once you have completed the remaining steps in this setup guide, you will be able to receive/process e-mail for the created domain(s).

#### Configuration of postfix

Once the application is fully configured, you need to copy some files to `/etc/postfix` and make some configuration changes to `/etc/postfix/main.cf`.

Copy the `pgsql-transport.cf` from `/home/mailguardian/mailguardian/configuration/examples/postfix` to `/etc/postfix` with `cp /home/mailguardian/mailguardian/configuration/examples/postfix/pgsql-transport.cf /etc/postfix/pgsql-transport.cf`

Then add the following lines to the bottom of `/etc/postfix/main.cf`

```
header_checks = regexp:/etc/postfix/header_checks
relay_domains = proxy:pgsql:/etc/postfix/pgsql-transport.cf
transport_maps = proxy:pgsql:/etc/postfix/pgsql-transport.cf
```

Next edit `/etc/postfix/pgsql-transport.cf` to match the credentials for your `PostgreSQL` installation and corresponding database.

If you wish to also allow SMTP relays, you can copy `home/mailguardian/mailguardian/configuration/examples/postfix/pgsql-mynetworks.cf` to `/etc/postfix/pgsql-mynetworks.cf` and edit the `PostgreSQL` credentials and corresponding database as well.

Then add this to your `/etc/postfix/main.cf` on the same line as `mynetworks = ...`

```
, proxy:pgsql:/etc/postfix/pgsql-mynetworks.cf
```

Finally create `/etc/postfix/header_checks` and insert this into the file:

```
/^Received:/ HOLD
```

Then restart `postfix` with `systemct restart postfix`

#### Configuration of MailScanner

At the moment, `postfix` should be delivering mail to `MailScanner`, which is scanning the messages according the the default configuration options. This means that nothing is happening.

We need to fix that, don't we?

First copy `MailGuardianConf.pm` from `/home/mailguardian/mailguardian/perl` to `/usr/share/MailScanner/perl/custom`
```
cp /home/mailguardian/mailguardian/perl/MailGuardianConf.pm /usr/share/MailScanner/perl/custom/MailGuardianConf.pm
```

Next edit `/usr/share/MailScanner/perl/custom/MailGuardianConf.pm` to match your credentials for the PostgreSQL database.

Then we need to create a link between the remaining files and MailScanner. The easiest way, so that you always have the latest version of the files, is to create a `symlink`.

```
ln -s /home/mailguardian/mailguardian/perl/MailGuardian.pm /usr/share/MailScanner/perl/custom
ln -s /home/mailguardian/mailguardian/perl/SQLBlackWhiteList.pm /usr/share/MailScanner/perl/custom
ln -s /home/mailguardian/mailguardian/perl/SQLSpamSettings.pm /usr/share/MailScanner/perl/custom
```

Next open `/etc/MailScanner/MailScanner.conf` and add/update the following settings:

```
Always Looked Up Last = &MailGuardianLogging
Run As User = postfix
Run As Group = postfix
Detailed Spam Report = yes
Quarantine Whole Message = yes
Quarantine Whole Messages As Queue Files = no
Include Scores In SpamAssassin Report = yes
Incoming Work User = postfix
Incoming Work Group = mtagroup
Incoming Work Permissions = 0660
Quarantine User = postfix
Quarantine Group = mtagroup
Quarantine Permissions = 0644
Is Definitely Not Spam = &SQLWhitelist
Is Definitely Spam = &SQLBlacklist
Use SpamAssassin = &SQLNoScan
Required SpamAssassin Score = &SQLSpamScores
High SpamAssassin Score = &SQLHighSpamScores
Incoming Queue Dir = /var/spool/postfix/hold
Outgoing Queue Dir = /var/spool/postfix/incoming
MTA = postfix
SpamAssassin User State Dir = /var/spool/MailScanner/spamassassin
```

Next we need to enable `MailScanner`, so that the server will actually start doing some work. Edit `/etc/MailScanner/defaults`and set `run_mailscanner=0` to `run_mailscanner=1` 

Next we configure the `Bayesian` Database by adding/updating the following in `/etc/MailScanner/spamassassin.conf`

```
bayes_path /etc/MailScanner/bayes/bayes
bayes_file_mode 0660
```

Then run these commands:

```
mkdir /etc/MailScanner/bayes
chown postfix:mtagroup /etc/MailScanner/bayes
chmod g+rws /etc/MailScanner/bayes
```

If `Bayesian` database data already exists for `root`, then we copy it over:

```
 cp /root/.spamassassin/bayes_* /etc/MailScanner/bayes
 chown postfix:mtagroup /etc/MailScanner/bayes/bayes_*
 chmod g+rw /etc/MailScanner/bayes/bayes_*
```

Next we verify the configuration files and functionality of `SpamAssassin` with `spamassassin -D -p /etc/MailScanner/spamassassin.conf --lint`

Then run `MailScanner --lint` to make sure that MailScanner is also working as expected

Lastly restart `MailScanner` with `systemctl restart mailscanner`

## Congratulations!

We would like to congratulate you on completing the setup and configuration of our application and wish you the best of luck with the usage.
If you find any issues with the application, have requests for feature or find a security problem, please do not hesitate to create an issue here on GitHub and we will get back to you

## Extras

### Configure cron-job for LetsEncrypt renewal

As our installation script does not have the appropriate access rights to create a cron-job as `root` during installation, you need to create this manually.

Run `crontab -e` as `root` to open the cron-job list for `root`. Then paste in this line:

```
0 0,12 * * * python -c 'import random; import time; time.sleep(random.random() * 3600)' && certbot renew
```

Then save and exit

### Deploying multiserver

The application supports deployment in a mulitserver configuration, where mutliple servers form the technical platform. An example could be something like this:

- 1 server to handle the web frontend
- 1 PostgreSQL datbase server, where all nodes connect to
- 3 inbound MailScanner nodes, which are responsible for scanning and processing the incoming email before delivery to recipients as well as logging the messages to the database
- 2 outbound MailScanner nodes for handling scanning and processing of email going outbound from servers inside our network or from customers using our servers for checking their outgoing mail for spam

This setup would simply require you to split up the installation steps, as the server running `nginx`/`apache` and thereby the web interface, does not need a working `MailScanner` installation.
The same goes for the PostgreSQL server. This only stores the database

During deployment of the server for the webinterface `install.py` will ask your server is part of multiserver setup and if it is responsible for the web interface. It will then make the appropriate configuration changes to handle this type of setup.

For the `MailScanner` nodes you would also reply `Y` to the multiserver deployment option in `install.py`, but reply `n` for the web frontend.

### Programmatically generate authentication tokens
You can programmatically generate authentication tokens, if you do not have one for a given user.
Run `python src/manage.py shell` and then execute this code to generate tokens for users that do currently not have one

```
from core.models import User
from rest_framework.authtoken.models import Token

users = User.objects.all()
for user in users:
    token, created = Token.objects.get_or_create(user=user)
    print(user.username, token.key)

```

### Custom cronjob timing
If you for some reason, wish to customize when your cronjobs run, you just need to replace the magic `@interval` with the normal cron syntax.

This is the crontab you have if you have followed the installation guide:

```
@hourly /home/mailguardian/mailguardian/bin/python /home/mailguardian/mailguardian/src/manage.py runjobs hourly
@daily /home/mailguardian/mailguardian/bin/python /home/mailguardian/mailguardian/src/manage.py runjobs daily
@weekly /home/mailguardian/mailguardian/bin/python /home/mailguardian/mailguardian/src/manage.py runjobs weekly
@monthly /home/mailguardian/mailguardian/bin/python /home/mailguardian/mailguardian/src/manage.py runjobs monthly
```

Let us now change the hourly cronjob to run at 5th minute of every hour, which means that it would run at 01:05AM, 02:05AM, 03:05AM etc. instead of running 01:00AM, 02:00AM, 03:00AM etc.
Change this:

```
@hourly /home/mailguardian/mailguardian/bin/python /home/mailguardian/mailguardian/src/manage.py runjobs hourly
```

To this:

```
5 * * * * /home/mailguardian/mailguardian/bin/python /home/mailguardian/mailguardian/src/manage.py runjobs hourly
```

Next let us change the daily cron job to run at 03:00 AM instead of the default 00:00AM.
Change this:

```
@daily /home/mailguardian/mailguardian/bin/python /home/mailguardian/mailguardian/src/manage.py runjobs daily
```

To this:

```
0 3 * * * /home/mailguardian/mailguardian/bin/python /home/mailguardian/mailguardian/src/manage.py runjobs daily
```

While we are at it, let us also change the weekly cronjob to run at 04:00AM every week on sundays.
Change this:

```
@weekly /home/mailguardian/mailguardian/bin/python /home/mailguardian/mailguardian/src/manage.py runjobs weekly
```

To this:

```
0 4 * * 0 /home/mailguardian/mailguardian/bin/python /home/mailguardian/mailguardian/src/manage.py runjobs weekly
```

Finally, let us reschedule the monthly cron job for running at 01:00AM the first day in every month:

Change this:

```
@monthly /home/mailguardian/mailguardian/bin/python /home/mailguardian/mailguardian/src/manage.py runjobs monthly
```

To this:

```
0 4 * */1 * /home/mailguardian/mailguardian/bin/python /home/mailguardian/mailguardian/src/manage.py runjobs monthly
```

### Increasing the size limit for when message scan is skipped
Change the `Max SpamAssassin Size` and `Max Spam Check Size` of `/etc/MailScanner/MailScanner.conf` and restart `MailScanner`. Be careful not to set this to high, as bigger messages will increase the processing time for `SpamAssassin` when evaluating a large message.

### Transport log data is not populating on messages
This is related to the permissions set on the mail log. Often these files are own by root and some administrative group.
The easy fix is simply to make your `mailguardian` application user to a member of the given group. This can however introduce some security risks if the given user account is compromised.

Another option is to create a cronjob for `root`, so that the log synchronization can be executed as `root`. This eliminates the problem in a farily simple way. The cronjob to create would look like this:

```
@hourly /home/mailguardian/mailguardian/bin/python /home/mailguardian/mailguardian/src/manage.py runjobs hourly > /dev/null 2>&1
```

The final option, which would be the most secure option, although a bit more complicated to configure, is to change the settings for `log rotation`. This would allow you to set the permissions of the log file when it is being rotated by the operating system and thereby allow you to set just enough permissions for allowing the `mailguardian` application user to read the logfile.