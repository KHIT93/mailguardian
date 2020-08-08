# MailGuardian
A Django-based RESTful SPA (Single Page Application) web GUI for MailScanner.

MailGuardian is your choice no matter if you need a single instance MailScanner deployment for your internal business email services or if you are a commercial hosting company, looking for a modern, reliable and scalable solution for letting you, your staff and your customers easily manage their spam filter appliance.

## Features

- Built in modern technology 
- Modern web interface that works great on your computer, phone or tablet
- RESTful API for easy integration with other applications
- Multi-node compatible, to allow running multiple MailScanner appliances with one web interface to manage them all
- Three user levels to easily manage access rights

## Supported browsers

- Microsoft Edge 12 or newer
- Mozilla Firefox 21 or newer
- Google Chrome 23 or newer
- Apple Safari 6 or newer for macOS/OSX
- Android 7 or newer
- iOS 10 or newer

## Requirements

### Hardware

We recommend the following requirements for your hardware, regardless of whether you are running with a physical machine or a virtual machine

- 2 CPU cores
- 4GB of RAM (This will vary greatly based on your database size and how much email that you are processing)
- 20GB of SAS storage or SSD storage

Please note that these requirements are for the full single-node deployment and does therefore also include the resources necessary for `MailScanner`and `SpamAssassin`etc.

### Software

- Debian 10 `Buster`, Ubuntu 18.04, Ubuntu 20.04, CentOS 7 or CentOS 8
- Python 3.6 or newer
- Python `virtualenv`
- PostgreSQL 12.x
- Postfix 3.3+ with `pgsql` driver
- Nginx 1.10+ or Apache 2.4+ with `HTTP/2` support
- `sudo` installed and configured on your system
- EPEL repository for CentOS
- Backports for Debian

Most requirements are handled by our installation script, but are listed in case that you want to install on an unsupported version or distribution, since this is technically possible as long as `MailScanner`, `SpamAssassin` and their dependencies will run.

### Optional requirements

- DataDumper library for `perl` for debugging (libdata-dumper-simple-perl)

## Getting started

Welcome to the MailGuardian documentation. We are glad that you have chosen our applicatin to manage your MailScanner deployment. We have made it unbelievably easy to deploy and manage your own professional spam filtering appliance.
For this to be as easy as possible, we have made the below instructions for the more technical parts of the deployment, to ensure that most people can follow along and get started.

To help you get started quickyl, we have a simple installation script, which will take care of everything for you. Simply run the lines below as root on your system

```
wget https://raw.githubusercontent.com/KHIT93/mailguardian/feature-new-install-scripts/installer.sh
bash installer.sh
```

We will ask you some questions during the installation and the rest will be automated

### Initial setup in the browser

Once the installation script, `install.py`, has completed, it is time to perform the final steps of the setup and create our application administrator account. To perform the final steps and start using the application, please visit the URL given at the end of the installation script.
Once you visit the given URL, you will automatically be redirected to the setup screen.

Complete the setup wizard and then log in to the application.

As you will not be able to process any mail without valid domains, you need to go to the `Domains` menu item and create your first domain.

That's it. Once you have completed the remaining steps in this setup guide, you will be able to receive/process e-mail for the created domain(s).

## Congratulations!

We would like to congratulate you on completing the setup and configuration of our application and wish you the best of luck with the usage.
If you find any issues with the application, have requests for feature or find a security problem, please do not hesitate to create an issue here on GitHub and we will get back to you

## Extras

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
This is related to the permissions set on the mail log. Often these files are owned by root and some administrative group.
The easy fix is simply to make your `mailguardian` application user to a member of the given group. This can however introduce some security risks if the given user account is compromised.

Another option is to create a cronjob for `root`, so that the log synchronization can be executed as `root`. This eliminates the problem in a farily simple way. The cronjob to create would look like this:

```
@hourly /home/mailguardian/mailguardian/bin/python /home/mailguardian/mailguardian/src/manage.py runjob mail process_mta_log > /dev/null 2>&1
```

This job is also what we create in our installation script

The final option, which would be the most secure option, although a bit more complicated to configure, is to change the settings for `log rotation`. This would allow you to set the permissions of the log file when it is being rotated by the operating system and thereby allow you to set just enough permissions for allowing the `mailguardian` application user to read the logfile.

### SMTP using STARTTLS
Edit `/etc/postfix/main.cf` and add this:

```
smtpd_tls_security_level = may
smtp_tls_security_level = may
smtpd_tls_mandatory_protocols = !SSLv2,!SSLv3,!TLSv1
smtp_tls_mandatory_protocols  = !SSLv2,!SSLv3,!TLSv1
smtpd_tls_protocols           = !SSLv2,!SSLv3,!TLSv1
smtp_tls_protocols            = !SSLv2,!SSLv3,!TLSv1
smtpd_tls_exclude_ciphers     = aNULL, LOW, EXP, MEDIUM, ADH, AECDH, MD5, DSS, ECDSA, CAMELLIA128, 3DES, CAMELLIA256, RSA+AES, eNULL
```

During the usage of our installation script, we configure the script to handle encrypted connections only on `TLSv1.2` and `TLSv1.3`