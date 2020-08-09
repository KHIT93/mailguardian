#!/usr/bin/env python3
#
# MailGuardian installation script
#
import os
import sys
import platform
import pytz
import json
import subprocess
import configparser
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f','--config-file', help='Input path to environment configuration file')

args = parser.parse_args()

if __name__ == "__main__":
    os.system('clear')
    # First make sure that we are running on Linux
    if platform.system() != 'Linux':
        print('Your operation system is not supported. MailGuardian can only run on Linux')
        exit(255)
    # Get the current directory of this script to determine the path to use for the systemd unit file templates
    APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Define some paths needed later
    SYSTEMD_PATH = '/etc/systemd/system/'
    NGINX_PATH = None
    NGINX_EXTENSION = ''
    PKG_MGR = None
    OPENSSL_BIN = which('openssl') or subprocess.check_output('which openssl', shell=True).strip().decode()
    NGINX_BIN = which('nginx') or subprocess.check_output('which nginx', shell=True).strip().decode()
    SYSTEMCTL_BIN = which('systemctl') or subprocess.check_output('which systemctl', shell=True).strip().decode()
    # Define some variables to store whether we need to skip some steps
    CONFIGURE_NGINX = True
    CONFIGURE_SYSTEMD = True
    CONFIGURE_CERTBOT = True
    HTTP_SECURE = True
    # Define variables to store generic data for use regardless of the installation purpose
    APP_HOSTNAME = platform.node()
    APP_USER = 'mailguardian'
    RETENTION_DAYS = 60
    DB_HOST = None
    DB_USER = None
    DB_PASS = None
    DB_NAME = None
    DB_PORT = None
    DB_SSL = True
    TZ = None
    PRIVKEY_PATH = APP_DIR + '/' + APP_HOSTNAME + '.key'
    CSR_PATH = APP_DIR + '/' + APP_HOSTNAME + '.csr'
    CERT_PATH = APP_DIR + '/' + APP_HOSTNAME + '.crt'
    DHPARAM_PATH = APP_DIR + '/dhparam.pem'
    # Stuff related to mulit-node configurations
    MULTI_NODE = False
    API_ONLY_MODE = False
    # Define some variables to use for processing nodes
    # These will be relevant for a single-node deployment,
    # as well as a multi-node deployment
    MTA = 'postfix'
    MTA_LOG = "/var/log/mail.log"
    MS_CONF_DIR = '/etc/MailScanner'
    MS_BIN = which('MailScanner') or '/usr/sbin/MailScanner'
    MS_LIB = '/usr/lib/MailScanner'
    MS_SHARED = '/usr/share/MailScanner'
    MS_QUARANTINE_DIR = "/var/spool/MailScanner/quarantine"
    SALEARN_BIN = which('sa-learn') or '/usr/local/bin/sa-learn'
    SA_BIN = which('spamassassin') or '/usr/local/bin/spamassassin'
    SA_RULES_DIR = '/var/lib/spamassassin'
    SENDMAIL_BIN = which('sendmail') or '/usr/sbin/sendmail'
    POSTQUEUE_BIN = which('postqueue') or '/usr/sbin/postqueue'
    # Detect the Linux distribution
    # If we can detect you specific Linux distribution,
    # we will skip the parts where we configure systemd,
    # and your webserver
    distro = 'LINUX'
    distro_version = '0'
    distro_version_codename = 'Core'
    with open('/etc/os-release', 'r') as f:
        for l in f.readlines():
            if l[:3] == 'ID=':
                distro = l.replace('ID=','').replace('"', '').strip()
            if l[:11] == 'VERSION_ID=':
                distro_version = l.replace('VERSION_ID=', '').replace('"', '').strip()
            if l[:17] == 'VERSION_CODENAME=':
                distro_version_codename = l.replace('VERSION_CODENAME=', '').replace('"', '').strip()
    if distro == 'centos':
        PKG_MGR = which('yum')
        NGINX_PATH = '/etc/nginx/conf.d/'
        NGINX_EXTENSION = '.conf'
    elif distro == 'debian':
        PKG_MGR = which('apt')
        if distro_version in ['9', '10']:
            NGINX_PATH = '/etc/nginx/sites-enabled/'
        else:
            print('Your version of Debian is not supported')
    elif distro.lower() == 'ubuntu':
        PKG_MGR = which('apt')
        if distro_version in ['16.04', '18.04', '20.04']:
            NGINX_PATH = '/etc/nginx/sites-enabled/'
        else:
            print('Your version of Ubuntu is not supported')
    else:
        print('Your Linux distribution or version is not supported')
        print(distro)
        exit(255)
    os.system('clear')
    print('We will now ask you a series of questions to properly configure the application for you')
    print('Do not worry, as we will not make any changes before all questions have been answered and confirmed by you')

    while True:
        APP_USER_INPUT = input('What is the username of the user running the MailGuardian application? [{0}] '.format(APP_USER))
        if APP_USER_INPUT != '' and APP_USER_INPUT is not None:
            APP_USER = APP_USER_INPUT
            break
        elif APP_USER != '' or APP_USER is not None:
            break

    while True:
        RETENTION_DAYS_INPUT = input('As your system will use quite a bit of space, could you please let us know how many days you want us to keep data in the system? [{0}] '.format(RETENTION_DAYS))
        if RETENTION_DAYS_INPUT != '' and RETENTION_DAYS_INPUT is not None:
            RETENTION_DAYS = RETENTION_DAYS_INPUT
            break
        elif RETENTION_DAYS != '' and RETENTION_DAYS is not None:
            break

    print('Next we need to get access to the database')
    
    while DB_HOST == '' or DB_HOST is None:
        DB_HOST = input('Please provide us the hostname of your PostgreSQL database server [localhost]: ')
        if DB_HOST == '':
            DB_HOST = 'localhost'
    print(chr(13))
    while DB_USER is None:
        DB_USER = input('Please provide us the username of the PostgreSQL user that has access to the database [mailguardian]: ')
        if DB_USER == '':
            DB_USER = 'mailguardian'
    print(chr(13))
    if not DB_HOST in ['localhost', '127.0.0.1']:
        while DB_PASS is None:
            DB_PASS = input('Please provide us the password for the PostgreSQL user specified above: ')
            if DB_PASS == '':
                DB_PASS = None
    else:
        DB_PASS = os.environ.get('ENV_DB_PASS')
    print(chr(13))
    while DB_NAME is None:
        DB_NAME = input('Please provide us the name of the PostgreSQL database [mailguardian]: ')
        if DB_NAME == '':
            DB_NAME = 'mailguardian'
    print(chr(13))
    DB_PORT_INPUT = input('Please provide us the TCP port on which PostgreSQL is listening. To use the default port, just press Enter. Otherwise input the port: ')
    if DB_PORT_INPUT != '' and DB_PORT_INPUT is not None:
        DB_PORT = DB_PORT_INPUT
    else:
        DB_PORT = 5432
    print(chr(13))
    
    os.system('clear')

    APP_HOSTNAME_INPUT = input('Please provide us with the hostname on which your MailGuardian instance will be accessible [%s]: ' % APP_HOSTNAME)
    if APP_HOSTNAME_INPUT != '' and APP_HOSTNAME_INPUT is not None:
        APP_HOSTNAME = APP_HOSTNAME_INPUT

    if input('Would you like to enable HTTP/2 and SSL/TLS (HTTPS) encryption for this instance? (Y/n) ').lower() != 'y':
        HTTP_SECURE = False

    if input('Should this server be part of a configuration that contains multiple servers? (y/N) ').lower() == 'y':
        MULTI_NODE = True
        print(chr(13))
        if input('Is this the server running the webinterface for users and administrators? (y/N) ').lower() == 'y':
            API_ONLY_MODE = False
        else:
            API_ONLY_MODE = True
    else:
        API_ONLY_MODE = False
    
    os.system('clear')
    if not MULTI_NODE or API_ONLY_MODE:
        MS_CONF_DIR_INPUT = input('Where are your MailScanner configuration files located? [{0}] '.format(MS_CONF_DIR))
        if MS_CONF_DIR_INPUT != '' and MS_CONF_DIR_INPUT is not None:
            MS_CONF_DIR = MS_CONF_DIR_INPUT
        os.system('clear')
        MS_BIN_INPUT = input('Please specify the full path to the MailScanner executable file/binary? [{0}] '.format(MS_BIN))
        if MS_BIN_INPUT != '' and MS_BIN_INPUT is not None:
            MS_BIN = MS_BIN_INPUT
        os.system('clear')
        MS_LIB_INPUT = input('Where are the MailScanner application libraries located? [{0}] '.format(MS_LIB))
        if MS_LIB_INPUT != '' and MS_LIB_INPUT is not None:
            MS_LIB = MS_LIB_INPUT
        os.system('clear')
        MS_SHARED_INPUT = input('Please let us know where your MailScanner shared resources are located [{0}] '.format(MS_SHARED))
        if MS_SHARED_INPUT != '' and MS_SHARED_INPUT is not None:
            MS_SHARED = MS_SHARED_INPUT
        os.system('clear')
        SALEARN_BIN_INPUT = input('To correctly handle SPAM, could you please let us know where your \'sa-learn\' binary is located? [{0}] '.format(SALEARN_BIN))
        if SALEARN_BIN_INPUT != '' and SALEARN_BIN_INPUT is not None:
            SALEARN_BIN = SALEARN_BIN_INPUT
        os.system('clear')
        SA_BIN_INPUT = input('To correctly handle SPAM, could you please let us know where your \'spamassassin\' binary is located? [{0}] '.format(SA_BIN))
        if SA_BIN_INPUT != '' and SA_BIN_INPUT is not None:
            SA_BIN = SA_BIN_INPUT
        os.system('clear')
        SA_RULES_DIR_INPUT = input('Please type in the location of your SpamAssassin rules configuration [{0}] '.format(SA_RULES_DIR))
        if SA_RULES_DIR_INPUT != '' and SA_RULES_DIR_INPUT is not None:
            SA_RULES_DIR = SA_RULES_DIR_INPUT
    
    installer_config = configparser.ConfigParser()
    installer_config['mailguardian'] = {
        'app_dir': APP_DIR,
        'hostname': APP_HOSTNAME,
        'https': HTTP_SECURE
    }
    installer_config['database'] = {
        'host': DB_HOST,
        'user': DB_USER,
        'pass': DB_PASS,
        'name': DB_NAME,
        'port': DB_PORT,
        'fqdn': DB_HOST + ':' + DB_PORT if str(DB_PORT) != '5432' else DB_HOST
    }
    installer_config['mailscanner'] = {
        'bin': MS_BIN,
        'config': MS_CONF_DIR,
        'shared': MS_SHARED,
        'lib': MS_LIB,
        'quarantine': MS_QUARANTINE_DIR
    }
    installer_config['spamassassin'] = {
        'sa_learn': SALEARN_BIN,
        'bin': SA_BIN,
        'rules': SA_RULES_DIR
    }

    with open(args.config_file, 'w') as f:
        installer_config.write(f)
