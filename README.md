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

### Optional requirements

- NodeJS, if you want to compile the assets from the sourcecode
- DataDumper library for `perl` for debugging (libdata-dumper-simple-perl)

## Getting started

Welcome to the Mailware documentation. We are glad that you have chosen our applicatin to manage your MailScanner deployment. We have made it unbelievably easy to deploy and manage your own professional spam filtering appliance.
For this to be as easy as possible, we have made the below instructions for the more technical parts of the deployment, to ensure that most people can follow along and get started.

### Prerequisites

Before we start deployment of Mailware, we need to have some software installed on our system. This guide currently provides instructions for Debian 9 `Stretch`, but we will also provide commands for CentOS 7. In the meantime, you can refer to the above requirements for what to install.
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
easy_install virtualenv pip
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

Once the installation has finished, we need to configure the filesystem with the correct permissions. We can do this with the following commands:

```
chown -R postfix:mtagroup /var/spool/MailScanner/spamassassin
chown -R postfix:postfix /var/spool/MailScanner/incoming
chown -R postfix:postfix /var/spool/MailScanner/quarantine
chmod -R g+r /var/spool/postfix/{hold,incoming}
```

Next we add some additional folders and then we can get started on actually installing and configuring our application to run.

```
mkdir -p /var/spool/MailScanner/spamassassin/
mkdir /etc/MailScanner/bayes
chown root:mtagroup /etc/MailScanner/bayes
chmod g+rws /etc/MailScanner/bayes
```

### Installation of Mailware

#### Creating the system user

Next, we will create a user, from which we will run our application

```
adduser mailware
```

Follow the onscreen prompt to complete the account creation and set a password.

Next we need to assign the new `mailware` user to the `mtagroup`, so that we can read the message queue and perform operations on the queue

```
usermod -a -G mtagroup mailware
```

#### Installing CPAN modules

This next step is quite easy, as we need to install some `perl modules` using `CPAN`:

```
cpan -i CPAN
cpan -i Data::Dumper
cpan -i Data::UUID
cpan -i DBI
cpan -i DBD::Pg
cpan -i Encoding::FixLatin
cpan -i Digest::SHA1
cpan -i Mail::ClamAV
cpan -i SAVI
```

#### Downloading the application

Next we need to download the application from https://github.com/KHIT93/mailware/releases

You can choose to download the sources and then compile the frontend assets (CSS and JavaScript) yourself, or you can download a prebuilt package, where these things are already done. We will cover installation from the prebuilt package.

Right click the link to the prebuilt package mailware-X.Y.Z.tar.gz and copy the link.

Run the following commands to download and extract the application:

```
su - mailware
wget https://github.com/KHIT93/mailware/releases/download/X.Y.Z/mailware-X.Y.Z.tar.gz
tar xvzf mailware-X.Y.Z.tar.gz
```

This should now create a new folder called `mailware` inside `/home/mailware`

#### Creating the Python Virtual Environment

Now that we have downloaded the application, we need to transform the code into a virtual environment for `python` to use, so that any other `python` applications on the system are not affected by the dependencies of this application

```
virtualenv -p python3 /home/mailware/mailware
```

Once this completes, we need to enter the virtual environment and install the `python packages` that are required for the application to run

```
cd /home/mailware/mailware
source bin/activate
```

Your prompt should now look something like this:
```
(mailware) mailware@localhost:~/mailware$
```

Now we run `pip install -r requirements.txt` to install the necessary `python` packages and libraries that are required for the application to run.

Next we need to install `WSGI` server to run our application. We do not provide one by default, but all our examples and prebuilt scripts asume that we will use `gunicorn`.

You can install `gunicorn` with `pip install gunicorn`.

#### Initializing the application and configuring your webserver

Now that our virtual environment is configured and ready, we need to run `install.py` so that we can get the webserver configured and prepared the application for first start.
The wizard that we start with `python install.py` will ask a series of questions regarding your server configuration and your usage of SSL/TLS certificates. We do this so that the application is secure by default and to support modern technologies like `HTTP/2`, We do therefore provide a prebuilt `systemd` unit file for running the application as service on your system as well as a `nginx` configuration for connecting the webserver to the `unix socket` provided by `gunicorn`.

First run `deactivate` and the type `exit` to log out of the `mailware` account and then as `root` change to `home/mailware/mailware` and run `source bin/activate` and then run `python install.py` and follow the instructions to complete the initial steps of application deployment. As this generates some files and installs some applications, this process can take some time. As we generate a secure `Diffie–Hellman` key parameters of `4096` bits, this part alone can take up to 45 minutes and is a mandatory step, since we force the application to be secure by default.

During exeuction of `install.py`, we will try to guess the hostname of the application and provide you with a URL. This URL will allow you to access the application from your favorite web browser and run the final steps of the installation.

The last thing that we need to do before we can open our favorite web browser and finish the configuration, is to `reload` the configuration files for `nginx`.

To ensure that our configurations are correct and that all certificate files are stored in the correct locations, we first run `nginx -t` and if no errors show, then we run `systemctl reload nginx`.

That is it. Now you can access the application from your favorite web browser.

#### Initial setup in the browser

TO-DO

#### Configuration of postfix

Once the application is fully configured, you need to copy some files to `/etc/postfix` and make some configuration changes to `/etc/postfix/main.cf`.

Copy the `pgsql-transport.cf` from `/home/mailware/mailware/configuration/examples/postfix` to `/etc/postfix` with `cp /home/mailware/mailware/configuration/examples/postfix/pgsql-transport.cf /etc/postfix/pgsql-transport.cf`

Then add the following lines to the bottom of `/etc/postfix/main.cf`

```
relay_domains = proxy:pgsql:/etc/postfix/pgsql-transport.cf
transport_maps = proxy:pgsql:/etc/postfix/pgsql-transport.cf
```

Next edit `/etc/postfix/pgsql-transport.cf` to match the credentials for your `PostgreSQL` installation and corresponding database. Then restart `postfix` with `systemct restart postfix`

#### Configuration of MailScanner

At the moment, `postfix` should be delivering mail to `MailScanner`, which is scanning the messages according the the default configuration options. This means that nothing is happening.

We need to fix that, don't we?

First copy `MailwareConf.pm` from `/home/mailware/mailware/perl` to `/usr/share/MailScanner/perl/custom`
```
cp /home/mailware/mailware/perl/MailwareConf.pm /usr/share/MailScanner/perl/custom/MailwareConf.pm
```

Next edit `/usr/share/MailScanner/perl/custom/MailwareConf.pm` to match your credentials for the PostgreSQL database.

Then we need to create a link between the remaining files and MailScanner. The easiest way, so that you always have the latest version of the files, is to create a `symlink`.

```
ln -s /home/mailware/mailware/perl/Mailware.pm /usr/share/MailScanner/perl/custom
ln -s /home/mailware/mailware/perl/SQLBlackWhiteList.pm /usr/share/MailScanner/perl/custom
ln -s /home/mailware/mailware/perl/SQLSpamSettings.pm /usr/share/MailScanner/perl/custom
```

Next open `/etc/MailScanner/MailScanner.conf` and add/update the following settings:

```
Always Looked Up Last = &MailwareLogging
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
```

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

#### Configure cron-job for LetsEncrypt renewal

As our installation script does not have the appropriate access rights to create a cron-job as `root` during installation, you need to create this manually.

Run `crontab -e` as `root` to open the cron-job list for `root`. Then paste in this line:

```
0 0,12 * * * python -c 'import random; import time; time.sleep(random.random() * 3600)' && certbot renew
```

Then save and exit

#### Deploying multiserver

The application supports deployment in a mulitserver configuration, where mutliple servers form the technical platform. An example could be something like this:

- 1 server to handle the web frontend
- 1 PostgreSQL datbase server, where all nodes connect to
- 3 inbound MailScanner nodes, which are responsible for scanning and processing the incoming email before delivery to recipients as well as logging the messages to the database
- 2 outbound MailScanner nodes for handling scanning and processing of email going outbound from servers inside our network or from customers using our servers for checking their outgoing mail for spam

This setup would simply require you to split up the installation steps, as the server running `nginx`/`apache` and thereby the web interface, does not need a working `MailScanner` installation.
The same goes for the PostgreSQL server. This only stores the database

During deployment of the server for the webinterface `install.py` will ask your server is part of multiserver setup and if it is responsible for the web interface. It will then make the appropriate configuration changes to handle this type of setup.

For the `MailScanner` nodes you would also reply `Y` to the multiserver deployment option in `install.py`, but reply `n` for the web frontend.

## Congratulations!

We would like to congratulate you on completing the setup and configuration of our application and wish you the best of luck with the usage.
If you find any issues with the application, have requests for feature or find a security problem, please do not hesitate to create an issue here on GitHub and we will get back to you