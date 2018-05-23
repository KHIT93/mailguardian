# Mailware
A Django-based RESTful SPA (Single Page Application) web GUI for MailScanner.

Mailware is your choice no matter if you need a single instance MailScanner deployment for your internal business email services or if you are a commercial hosting company, looking for a modern, reliable and scalable solution for letting you, your staff and your customers easily manage their spam filter appliance.

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

### Optional requirements

- NodeJS, if you want to compile the assets from the sourcecode

## Getting started

Welcome to the Mailware documentation. We are glad that you have chosen our applicatin to manage your MailScanner deployment. We have made it unbelievably easy to deploy and manage your own professional spam filtering appliance.
For this to be as easy as possible, we have made the below instructions for the more technical parts of the deployment, to ensure that most people can follow along and get started.

### Prerequisites

Before we start deployment of Mailware, we need to have some software installed on our system. This guide currently provides instructions for Debian 9 `Stretch`, but we will also provide commands for CentOS 7. In the meantime, you can refer to the above requirements for what to install.

This means that we will be installing the following applications:

- `nginx`
- `postfix-pgsql`
- `openssl`
- `python3`
- `sudo`
- `MailScanner`

First we install what we can from the official Debian `repositories`:

```
apt install sudo wget postfix-pgsql python3 python3-setuptools libpq-dev nginx ca-certificates openssl
```

This will install most of the things that we need. Next we will add the official `PostgreSQL` repo to get the latest version of `PostgreSQL 10`

```
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
apt update
apt dist-upgrade
apt install postgresql-10 postgresql-sever-dev-10 postgresql-client-10
```

### Prepare MailScanner config on postfix after install

```
mkdir -p /var/spool/MailScanner/spamassassin/
chown -R postfix:mtagroup /var/spool/MailScanner/spamassassin
chown -R postfix:postfix /var/spool/MailScanner/incoming
chown -R postfix:postfix /var/spool/MailScanner/quarantine
chmod -R g+r /var/spool/postfix/{hold,incoming}
usermod -a -G mtagroup mailware
apt install postgresqlXX-server-dev libpq-dev libdata-dumper-simple-perl libpng-dev
cpan -i CPAN
cpan -i Data::Dumper
cpan -i Data::UUID
cpan -i DBI
cpan -i DBD::Pg
cpan -i Encoding::FixLatin
cpan -i Digest::SHA1
cpan -i Mail::ClamAV
cpan -i SAVI
mkdir /etc/MailScanner/bayes
chown root:mtagroup /etc/MailScanner/bayes
chmod g+rws /etc/MailScanner/bayes
```


```
$ sudo certbot certonly --authenticator standalone --pre-hook "systemctl stop nginx" --post-hook "systemctl start nginx"
```

```
0 0,12 * * * python -c 'import random; import time; time.sleep(random.random() * 3600)' && certbot renew 
```