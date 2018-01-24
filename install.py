#!/usr/bin/env python3
#
# Placeholder for MailWare installation script
#
import os
import sys
import platform
import pytz

if __name__ == "__main__":
    # Get the current directory of this script to determine the path to use for the systemd service unit files
    APP_DIR = os.path.dirname(os.path.abspath(__file__))
    # Set some variables to hold the information from the questions asked
    CONFIGURE_NGINX = True
    CONFIGURE_SYSTEMD = True
    CONFIGURE_CERTBOT = True
    HTTP_SECURE = True
    SYSTEMD_PATH = '/lib/systemd/system/'
    NGINX_PATH = None
    NGINX_EXTENSION = ''
    APP_USER = ''
    MTA = None
    MS_CONF_DIR = None
    MS_BIN = None
    MS_LIB = None
    MS_SHARED = None
    SALEARN_BIN = None
    SA_RULES_DIR = None
    RETENTION_DAYS = None
    DB_HOST = None
    DB_USER = None
    DB_PASS = None
    DB_PORT = None
    DB_SSL = True
    TZ = None
    API_ONLY_MODE = False
    # First detect operating system
    # If we can detect it, then we will ask questions to generate webserver and systemd service files
    # If we cannot detect it, then we show a warning and skip the steps regarding webserver and systemd
    if platform.system() != 'Linux':
        print('Your operation system is not supported. MailWare can only run on Linux')
        #exit()
    else:
        distro = platform.linux_distribution()
        if distro[0] == 'CentOS Linux':
            if int(distro[1].replace('.', '')) >= 730000:
                NGINX_PATH = '/etc/nginx/conf.d/'
                NGINX_EXTENSION = '.conf'
        elif distro[0] == 'debian':
            if int(distro[1].replace('.', '')) >= 90:
                NGINX_PATH = '/etc/nginx/sites-enabled/'
            else:
                print('Your version of Debian is not supported')
        elif distro[0] == 'Ubuntu':
            if int(distro[1].replace('.', '')) >= 1604:
                NGINX_PATH = '/etc/nginx/sites-enabled/'
            else:
                print('Your version of Ubuntu is not supported')
        else:
            print('Your Linux distribution or version is not supported')
            print(distro)
            exit()
    if input('Did you run \'pip install -r requirements.txt\' to before you started the installation scrpt (y/N) ').lower() == 'n':
         print('Please relaunch this script after running \'pip install -r requirements.txt\' ')
         exit()
    else:
        if os.geteuid() != 0:
            print('You need to run the installation script as root. With root elevation, we are unable to configure the system for you')
            print('You can still continue the execution of the installation script, but choose to leave out the parts that require root elevation')
            if input('Do you want to skip steps that require root elevation and allow the script to continue? (y/N) ').lower() == 'y':
                print('We will continue execution but skip the parts that require root elevation')
                CONFIGURE_CERTBOT = False
                CONFIGURE_NGINX = False
                CONFIGURE_SYSTEMD = False
            else:
                print('Please run the script again as root or with sudo, to elevate execution')
                exit()
        print('We will now ask you a series of questions to properly configure the application for you')
        print('Do not worry, as we will not make any changes before all questions have been answered and confirmed by you')
        while APP_USER == '':
            APP_USER = input('What is the username of the user running the Mailware application? ')
        # Next we need to ask some questions
        # to generate the correct mailware-env.json
        print('Available MTA\'s (Mail Transport Agent)')
        print('sendmail')
        print('postfix')
        print('exim')
        MTA = input('Which MTA do you want to use? [postfix] ')
        if MTA == '' or MTA is None:
            MTA = 'postfix'
        MS_CONF_DIR = input('Where are your MailScanner configuration files located? [/etc/MailScanner/] ')
        if MS_CONF_DIR == '' or MS_CONF_DIR is None:
            MS_CONF_DIR = '/etc/MailScanner/'
        MS_BIN = input('Please specify the full path to the MailScanner executable file/binary? [/usr/sbin/MailScanner] ')
        if MS_BIN == '' or MS_BIN is None:
            MS_BIN = '/usr/sbin/MailScanner'
        MS_LIB = input('Where are the MailScanner application libraries located? [/usr/lib/MailScanner/] ')
        if MS_LIB == '' or MS_LIB is None:
            MS_LIB = '/usr/lib/MailScanner/'
        MS_SHARED = input('Please let us know where your MailScanner shared resources are located [/usr/share/MailScanner/] ')
        if MS_SHARED == '' or MS_SHARED is None:
            MS_SHARED = '/usr/share/MailScanner/'
        SALEARN_BIN = input('To correctly handle SPAM, could you please let us know where your \'salearn\' binary is located? [/usr/bin/salearn] ')
        if SALEARN_BIN == '' or SALEARN_BIN is None:
            SALEARN_BIN = '/usr/bin/salearn'
        SA_RULES_DIR = input('Please type in the location of your SpamAssassin rules configuration [/usr/share/spamassassin/] ')
        if SA_RULES_DIR == '' or SA_RULES_DIR is None:
            SA_RULES_DIR = '/usr/share/spamassassin/'
        while not isinstance(RETENTION_DAYS, int):
            RETENTION_DAYS = input('As your system will use quite a bit of space, could you please let us know how many days you want us to keep data in the system? [60] ')
            if RETENTION_DAYS == '' or RETENTION_DAYS is None:
                RETENTION_DAYS = 60
        print('Next we need to get access to the database')
        while DB_HOST is None:
            DB_HOST = input('Please provide us the hostname of your PostgreSQL database server [localhost]: ')
            if DB_HOST == '':
                DB_HOST = 'localhost'
        while DB_USER is None:
            DB_USER input('Please provide us the username of the PostgreSQL user that has access to the database: ')
            if DB_USER == '':
                DB_USER = None
        while DB_PASS is None:
            DB_PASS = input('Please provide us the password for the PostgreSQL user specified above: ')
            if DB_PASS == '':
                DB_PASS = None
        DB_PORT = input('Please provide us the TCP port on which PostgreSQL is listening. To use the default port, just press. Otherwise input the port: ')
        if DB_PORT == '' or DB_PORT is None:
            while not isinstance(DB_PORT, int) and DB_PORT is not None and DB_PORT != '':
                DB_PORT = input('Please provide us the TCP port on which PostgreSQL is listening. To use the default port, just press. Otherwise input the port: ')
        if input('Does you PostgreSQL server support SSL (Y/n) '.lower() == 'n'):
            DB_SSL = False
        # Next we configure the timezone settings
        print('Please provide us with your timezone. This is usually the same as you chose during installation of your operating system. It is usually typed as Region/City. Fx. US/Eastern or Europe/Berlin')
        TZ = input('Please type in your timezone. To get a list of available timezones type ?. To use UTC, just press [Enter] ')
        if TZ == '?':
            for timezone in pytz.all_timezones:
                print(timezone)
        if TZ == '' or TZ is None:
            TZ = 'UTC'
        # Next choose your language (Only languages that are available for the application will be displayed)
        # This is ignored for now, as we do not have multilingual suppport at the moment
        if input('Should this server be part of a configuration that contains multiple servers? (y/N) ').lower() == 'y':
            if input('Is this the server running the webinterface for users and administrators? (y/n) ').lower() == 'y':
                API_ONLY_MODE = False
            else:
                API_ONLY_MODE = True
        else:
            API_ONLY_MODE = False
        if CONFIGURE_CERTBOT and CONFIGURE_NGINX and CONFIGURE_SYSTEMD:
            if os.geteuid() != 0:
                print('You are not running the installation with root privileges. The script will now terminate')
                exit()
            if input('Would you like to enable HTTP/2 and SSL/TLS (HTTPS) encryption for this instance? (Y/n) ').lower() != 'y':
                HTTP_SECURE = False
            if HTTP_SECURE:
                if input('Would you like us to automatically generate a LetsEncrypt certificate for you? (Y/n) ').lower() == 'y':
                    # Check if certbot is installed and  if not, then we install it
                    # Request a certificate and note the path
                    pass
                elif input('Do you want to use an existing certificate? (y/N) ').lower() == 'y':
                    PRIVKEY_PATH = input('Please provide us the path to your SSL/TLS private key: ')
                    CERT_PATH = input('Please provide the path for your SSL/TLS certificate: ')
                    if input('Does your certificate require an intermediate certification authority? (Y/n) ').lower() == 'y':
                        INTERMEDIATE_CA_PATH = input('Please provide the path to the intermediate CA certificate: ')
                else:
                    # Generate a new 4096-bit private key
                    # Generate a certificate signing request (CSR) and save the path so that we can output it at the end of the install script
                    # Save the path of the certificate for when we generate the nginx configuration file
                    pass
                # Generate a new 4096-bit DH-parameter file for more secure encryption
            # Generate nginx configuration file

            # Generate systemd service unit file

            # Enable systemd service units on startup

            if input('Should we start the MailWare services for you now? (Y/n) ').lower() == 'y':
                # Ask systemd to start mailware.service and mailware-celery.service
                pass
    print('The installation script has finished. Any errors that occurred during installation need to be fixed manually')
    print('Below is a list of files that we have created during the installation process. If you need to run the installation script again, then you can simply delete these files')
