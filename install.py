#!/usr/bin/env python3
#
# Placeholder for MailGuardian installation script
#
import os
import sys
import platform
import pytz
import json

def which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None

if __name__ == "__main__":
    # Get the current directory of this script to determine the path to use for the systemd service unit files
    APP_DIR = os.path.dirname(os.path.abspath(__file__))
    print(APP_DIR)
    # Get the machine FQDN
    APP_HOSTNAME = platform.node()
    # Set some variables to hold the information from the questions asked
    CONFIGURE_NGINX = True
    CONFIGURE_SYSTEMD = True
    CONFIGURE_CERTBOT = True
    HTTP_SECURE = True
    SYSTEMD_PATH = '/lib/systemd/system/'
    NGINX_PATH = None
    NGINX_EXTENSION = ''
    PKG_MGR = None
    OPENSSL_BIN = which('openssl')
    NGINX_BIN = which('nginx')
    SYSTEMCTL_BIN = which('systemctl')
    APP_USER = 'mailguardian'
    MTA = 'postfix'
    MTA_LOG = "/var/log/mail.log"
    MS_CONF_DIR = '/etc/MailScanner'
    MS_BIN = which('MailScanner')
    MS_LIB = '/usr/lib/MailScanner'
    MS_SHARED = '/usr/share/MailScanner'
    MS_QUARANTINE_DIR = "/var/spool/MailScanner/quarantine"
    SALEARN_BIN = which('salearn')
    SA_BIN = which('spamassassin')
    SA_RULES_DIR = '/var/lib/spamassassin'
    SENDMAIL_BIN = which('sendmail')
    RETENTION_DAYS = 60
    DB_HOST = None
    DB_USER = None
    DB_PASS = None
    DB_NAME = None
    DB_PORT = None
    DB_SSL = True
    TZ = None
    API_ONLY_MODE = False
    PRIVKEY_PATH = APP_DIR + '/' + APP_HOSTNAME + '.key'
    CSR_PATH = APP_DIR + '/' + APP_HOSTNAME + '.csr'
    CERT_PATH = APP_DIR + '/' + APP_HOSTNAME + '.crt'
    DHPARAM_PATH = APP_DIR + '/dhparam.pem'
    # First detect operating system
    # If we can detect it, then we will ask questions to generate webserver and systemd service files
    # If we cannot detect it, then we show a warning and skip the steps regarding webserver and systemd
    if platform.system() != 'Linux':
        print('Your operation system is not supported. MailGuardian can only run on Linux')
        #exit()
    else:
        distro = platform.linux_distribution()
        if distro[0] == 'CentOS Linux':
            PKG_MGR = which('yum')
            if int(distro[1].replace('.', '')) >= 730000:
                NGINX_PATH = '/etc/nginx/conf.d/'
                NGINX_EXTENSION = '.conf'
        elif distro[0] == 'debian':
            PKG_MGR = which('apt')
            if int(distro[1].replace('.', '')) >= 90:
                NGINX_PATH = '/etc/nginx/sites-enabled/'
            else:
                print('Your version of Debian is not supported')
        elif distro[0] == 'Ubuntu':
            PKG_MGR = which('apt')
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
            print('You need to run the installation script as root. Without root elevation, we are unable to configure the system for you')
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
        APP_USER_INPUT = input('What is the username of the user running the MailGuardian application? [{0}] '.format(APP_USER))
        if APP_USER_INPUT != '' or APP_USER_INPUT is not None:
            APP_USER = APP_USER_INPUT
        # Next we need to ask some questions
        # to generate the correct mailguardian-env.json
        print('Available MTA\'s (Mail Transport Agent)')
        print('sendmail')
        print('postfix')
        print('exim')
        MTA_INPUT = input('Which MTA do you want to use? [{0}] '.format(MTA))
        if MTA_INPUT == '' or MTA_INPUT is None:
            MTA = MTA_INPUT
        MS_CONF_DIR_INPUT = input('Where are your MailScanner configuration files located? [{0}] '.format(MS_CONF_DIR))
        if MS_CONF_DIR_INPUT != '' or MS_CONF_DIR_INPUT is not None:
            MS_CONF_DIR = MS_CONF_DIR_INPUT
        MS_BIN_INPUT = input('Please specify the full path to the MailScanner executable file/binary? [{0}] '.format(MS_BIN))
        if MS_BIN_INPUT != '' or MS_BIN_INPUT is not None:
            MS_BIN = MS_BIN_INPUT
        MS_LIB_INPUT = input('Where are the MailScanner application libraries located? [{0}] '.format(MS_LIB))
        if MS_LIB_INPUT != '' or MS_LIB_INPUT is not None:
            MS_LIB = MS_LIB_INPUT
        MS_SHARED_INPUT = input('Please let us know where your MailScanner shared resources are located [{0}] '.format(MS_SHARED))
        if MS_SHARED_INPUT != '' or MS_SHARED_INPUT is not None:
            MS_SHARED = MS_SHARED_INPUT
        SALEARN_BIN_INPUT = input('To correctly handle SPAM, could you please let us know where your \'salearn\' binary is located? [{0}] '.format(SALEARN_BIN))
        if SALEARN_BIN_INPUT != '' or SALEARN_BIN_INPUT is not None:
            SALEARN_BIN = SALEARN_BIN_INPUT
        SA_RULES_DIR_INPUT = input('Please type in the location of your SpamAssassin rules configuration [{0}] '.format(SA_RULES_DIR))
        if SA_RULES_DIR_INPUT != '' or SA_RULES_DIR_INPUT is not None:
            SA_RULES_DIR = SA_RULES_DIR_INPUT
        #while not isinstance(str(RETENTION_DAYS), int):
        RETENTION_DAYS_INPUT = input('As your system will use quite a bit of space, could you please let us know how many days you want us to keep data in the system? [{0}] '.format(RETENTION_DAYS))
        if RETENTION_DAYS_INPUT != '' or RETENTION_DAYS_INPUT is not None:
            RETENTION_DAYS = RETENTION_DAYS_INPUT
        print('Next we need to get access to the database')
        while DB_HOST is None:
            DB_HOST = input('Please provide us the hostname of your PostgreSQL database server [localhost]: ')
            if DB_HOST == '':
                DB_HOST = 'localhost'
        while DB_USER is None:
            DB_USER = input('Please provide us the username of the PostgreSQL user that has access to the database [mailguardian]: ')
            if DB_USER == '':
                DB_USER = 'mailguardian'
        while DB_PASS is None:
            DB_PASS = input('Please provide us the password for the PostgreSQL user specified above: ')
            if DB_PASS == '':
                DB_PASS = None
        while DB_NAME is None:
            DB_NAME = input('Please provide us the name of the PostgreSQL database [mailguardian]: ')
            if DB_NAME == '':
                DB_NAME = 'mailguardian'
        DB_PORT = input('Please provide us the TCP port on which PostgreSQL is listening. To use the default port, just press. Otherwise input the port: ')
        if DB_PORT == '' or DB_PORT is None:
            DB_PORT = 5432
            #while not isinstance(int(DB_PORT), int) and DB_PORT is not None and DB_PORT != '':
            #    DB_PORT = input('Please provide us the TCP port on which PostgreSQL is listening. To use the default port, just press. Otherwise input the port: ')
        if input('Does you PostgreSQL server support SSL (Y/n) '.lower() == 'n'):
            DB_SSL = False
        # Next we configure the timezone settings
        print('Please provide us with your timezone. This is usually the same as you chose during installation of your operating system. It is usually typed as Region/City. Fx. US/Eastern or Europe/Berlin')
        TZ = input('Please type in your timezone. To get a list of available timezones type ?. To use UTC, just press Enter: ')
        if TZ == '?':
            for timezone in pytz.all_timezones:
                print(timezone)
            TZ = input('Please type in your timezone. To get a list of available timezones type ?. To use UTC, just press Enter: ')
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
        env_contents = {
            "debug": False,
            "hostname": APP_HOSTNAME,
            "database": {
                "name": DB_NAME,
                "user": DB_USER,
                "password": DB_PASS,
                "host": DB_HOST,
                "port": DB_PORT,
                "options": {
                    "sslmode": "require" if DB_SSL else "prefer"
                },
                "language_code": "en_us",
                "time_zone": TZ,
                "api_only_mode": API_ONLY_MODE,
                "hostconfig": {
                    "salearn_bin": SALEARN_BIN,
                    "sa_bin": SA_BIN,
                    "mailscanner_bin": MS_BIN,
                    "mailscanner_config_dir": MS_CONF_DIR,
                    "mailscanner_share_dir": MS_SHARED,
                    "mailscanner_lib_dir": MS_LIB,
                    "tmp_dir": "/tmp",
                    "sa_rules_dir": SA_RULES_DIR,
                    "sendmail_bin": SENDMAIL_BIN,
                    "mailscanner_quarantine_dir": MS_QUARANTINE_DIR,
                    "mta_logfile": MTA_LOG
                },
                "retention": {
                    "records": RETENTION_DAYS,
                    "audit": RETENTION_DAYS,
                    "quarantine": RETENTION_DAYS
                },
                "audit_log": True,
                "mta": MTA,
                "branding": {
                    "name": "MailGuardian",
                    "tagline": "Securing your email",
                    "logo": ""
                }
            }
        }
        mailguardian_env_contents = json.dumps(env_contents)
        print(mailguardian_env_contents)
        print('The above is the configuration file that we will save to %s' % '')
        print('After this point everything we do is commited to disk immediately')
        if input('Is this correct and can we continue? (Y/n').lower() == 'n':
            print('Installation will be aborted. Please rerun the installation script to try again')
            exit()
        print('Writing configuration file %s' % APP_DIR + '/mailguardian-env.json')
        CONF_FILE = open(APP_DIR + '/mailguardian-env.json', 'w')
        CONF_FILE.write(mailguardian_env_contents)
        CONF_FILE.close()
        if CONFIGURE_CERTBOT and CONFIGURE_NGINX and CONFIGURE_SYSTEMD:
            if os.geteuid() != 0:
                print('You are not running the installation with root privileges. The script will now terminate')
                exit()
            APP_HOSTNAME = input('Please provide us with the hostname on which your MailGuardian instance will be accessible [%s]: ' % platform.node())
            if APP_HOSTNAME == '' or APP_HOSTNAME is None:
                APP_HOSTNAME = platform.node()
            if input('Would you like to enable HTTP/2 and SSL/TLS (HTTPS) encryption for this instance? (Y/n) ').lower() != 'y':
                HTTP_SECURE = False
            if HTTP_SECURE:
                if input('Would you like us to automatically generate a LetsEncrypt certificate for you? (Y/n) ').lower() == 'y':
                    # Check if certbot is installed and  if not, then we install it
                    if not which('certbot'):
                        os.system(PKG_MGR + ' install certbot -y')
                    # Request a certificate and note the path
                    PRIVKEY_PATH = '/etc/letsencrypt/live/{0}/privkey.pem'.format(APP_HOSTNAME)
                    CERT_PATH = '/etc/letsencrypt/live/{0}/fullchain.pem'.format(APP_HOSTNAME)
                    os.system(which('certbot') + ' certonly --standalone -d {0} --pre-hook "{1} stop nginx" --post-hook "{1} start nginx"'.format(APP_HOSTNAME, SYSTEMCTL_BIN))
                    print('If the certificate was successfully created, please make sure to manually add this cronjob using sudo crontab -e:')
                    print("0 6,18 * * * python -c 'import random; import time; time.sleep(random.random() * 3600)' && certbot renew")
                    print('This will make sure that we try to renew your LetsEncrypt Certificate twice a day and random minutes')
                elif input('Do you want to use an existing certificate? (y/N) ').lower() == 'y':
                    PRIVKEY_PATH = input('Please provide us the path to your SSL/TLS private key: ')
                    CERT_PATH = input('Please provide the path for your SSL/TLS certificate: ')
                    if input('Does your certificate require an intermediate certification authority? (Y/n) ').lower() == 'y':
                        INTERMEDIATE_CA_PATH = input('Please provide the path to the intermediate CA certificate: ')
                else:
                    # Save the path of the certificate for when we generate the nginx configuration file
                    PRIVKEY_PATH = APP_DIR + '/' + APP_HOSTNAME + '.key'
                    CSR_PATH = APP_DIR + '/' + APP_HOSTNAME + '.csr'
                    CERT_PATH = APP_DIR + '/' + APP_HOSTNAME + '.crt'
                    # Generate a new 4096-bit private key and CSR (Certificate Signing Request)
                    os.system(OPENSSL_BIN + ' req -new -newkey rsa:4096 -nodes -keyout {0} -out {1}'.format(PRIVKEY_PATH, CSR_PATH))
                # Generate a new 4096-bit DH-parameter file for more secure encryption
                os.system(OPENSSL_BIN + ' dhparam -out {0} 4096'.format(DHPARAM_PATH))
            # Generate nginx configuration file
            NGINX_TMPL = open(APP_DIR + '/examples/nginx/domain.tld', 'r')
            NGINX_CONF = NGINX_TMPL.read()
            NGINX_TMPL.close()
            if HTTP_SECURE:
                NGINX_CONF = NGINX_CONF.replace('/home/mailguardian/cert/domain.tld.crt', CERT_PATH).replace('/home/mailguardian/cert/domain.tld.key', PRIVKEY_PATH).replace('/home/mailguardian/cert/dhparam.pem', DHPARAM_PATH)
            else:
                NGINX_CONF = NGINX_CONF.replace('listen 443 ssl http2;', '# listen 443 ssl http2;').replace('if ($scheme = "http") { set $redirect_https 1; }','# if ($scheme = "http") { set $redirect_https 1; }').replace('if ($request_uri ~ ^/.well-known/acme-challenge/) { set $redirect_https 0; }', '# if ($request_uri ~ ^/.well-known/acme-challenge/) { set $redirect_https 0; }').replace('if ($redirect_https) { rewrite ^ https://$server_name$request_uri? permanent; }', '# if ($redirect_https) { rewrite ^ https://$server_name$request_uri? permanent; }').replace('ssl on;','# ssl on;').replace('ssl_certificate /home/mailguardian/cert/domain.tld.crt;','# ssl_certificate /home/mailguardian/cert/domain.tld.crt;').replace('ssl_certificate_key /home/mailguardian/cert/domain.tld.key;','# ssl_certificate_key /home/mailguardian/cert/domain.tld.key;').replace('ssl_dhparam /home/mailguardian/cert/dhparam.pem;', '# ssl_dhparam /home/mailguardian/cert/dhparam.pem;').replace('ssl_session_cache shared:SSL:50m;','# ssl_session_cache shared:SSL:50m;').replace('ssl_session_timeout 30m;','# ssl_session_timeout 30m;').replace('ssl_protocols TLSv1.1 TLSv1.2;','# ssl_protocols TLSv1.1 TLSv1.2;').replace('ssl_ciphers "EECDH+ECDSA+AESGCM EECDH+aRSA+AESGCM EECDH+ECDSA+SHA384 EECDH+ECDSA+SHA256 EECDH+aRSA+SHA384 EECDH+aRSA+SHA256 EECDH+aRSA+RC4 EECDH EDH+aRSA !aNULL !eNULL !LOW !3DES !MD5 !EXP !PSK !SRP !DSS";','# ssl_ciphers "EECDH+ECDSA+AESGCM EECDH+aRSA+AESGCM EECDH+ECDSA+SHA384 EECDH+ECDSA+SHA256 EECDH+aRSA+SHA384 EECDH+aRSA+SHA256 EECDH+aRSA+RC4 EECDH EDH+aRSA !aNULL !eNULL !LOW !3DES !MD5 !EXP !PSK !SRP !DSS";').replace('ssl_prefer_server_ciphers on;','# ssl_prefer_server_ciphers on;')
            NGINX_CONF = NGINX_CONF.replace('domain.tld', APP_HOSTNAME).replace('/home/mailguardian/app', APP_DIR)
            NGINX_FILE = open(NGINX_PATH + APP_HOSTNAME + NGINX_EXTENSION, 'w')
            NGINX_FILE.write(NGINX_CONF)
            NGINX_FILE.close()
            # Generate systemd service unit file
            SYSTEMD_TMPL = open(APP_DIR + '/examples/systemd/mailguardian.service', 'r')
            SYSTEMD_UNIT = SYSTEMD_TMPL.read()
            SYSTEMD_UNIT = SYSTEMD_UNIT.replace('/home/mailguardian/app', APP_DIR).replace('mailguardian', APP_USER)
            SYSTEMD_FILE = open(SYSTEMD_PATH + 'mailguardian.service', 'w')
            SYSTEMD_FILE.write(SYSTEMD_UNIT)
            SYSTEMD_FILE.close()
            # Reload systemd unit cache
            os.system(SYSTEMCTL_BIN + ' daemon-reload')
            # Enable systemd service units on startup
            os.system(SYSTEMCTL_BIN + ' enable mailguardian.service')
            if input('Should we start the MailGuardian services for you now? (Y/n) ').lower() == 'y':
                # Ask systemd to start mailguardian.service and mailguardian-celery.service
                os.system(SYSTEMCTL_BIN + ' start mailguardian.service')
    print('The installation script has finished. Any errors that occurred during installation need to be fixed manually')
    print('Below is a list of files that we have created during the installation process. If you need to run the installation script again, then you can simply delete these files')
