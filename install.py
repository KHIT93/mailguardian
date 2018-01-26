#!/usr/bin/env python3
#
# Placeholder for MailWare installation script
#
import os
import sys
import platform
import pytz

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
    OPENSSL_BIN = '/usr/bin/openssl'
    NGINX_BIN = '/usr/sbin/nginx'
    SYSTEMCTL_BIN = '/usr/bin/systemctl'
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
        print('Your operation system is not supported. MailWare can only run on Linux')
        #exit()
    else:
        distro = platform.linux_distribution()
        if distro[0] == 'CentOS Linux':
            PKG_MGR = '/usr/bin/yum'
            if int(distro[1].replace('.', '')) >= 730000:
                NGINX_PATH = '/etc/nginx/conf.d/'
                NGINX_EXTENSION = '.conf'
        elif distro[0] == 'debian':
            PKG_MGR = '/usr/bin/apt'
            if int(distro[1].replace('.', '')) >= 90:
                NGINX_PATH = '/etc/nginx/sites-enabled/'
            else:
                print('Your version of Debian is not supported')
        elif distro[0] == 'Ubuntu':
            PKG_MGR = '/usr/bin/apt'
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
        #while not isinstance(str(RETENTION_DAYS), int):
        RETENTION_DAYS = input('As your system will use quite a bit of space, could you please let us know how many days you want us to keep data in the system? [60] ')
        if RETENTION_DAYS == '' or RETENTION_DAYS is None:
            RETENTION_DAYS = 60
        print('Next we need to get access to the database')
        while DB_HOST is None:
            DB_HOST = input('Please provide us the hostname of your PostgreSQL database server [localhost]: ')
            if DB_HOST == '':
                DB_HOST = 'localhost'
        while DB_USER is None:
            DB_USER = input('Please provide us the username of the PostgreSQL user that has access to the database: ')
            if DB_USER == '':
                DB_USER = None
        while DB_PASS is None:
            DB_PASS = input('Please provide us the password for the PostgreSQL user specified above: ')
            if DB_PASS == '':
                DB_PASS = None
        while DB_NAME is None:
            DB_NAME = input('Please provide us the name of the PostgreSQL database: ')
            if DB_NAME == '':
                DB_NAME = None
        DB_PORT = input('Please provide us the TCP port on which PostgreSQL is listening. To use the default port, just press. Otherwise input the port: ')
        if DB_PORT == '' or DB_PORT is None:
            DB_PORT = 5432
            #while not isinstance(int(DB_PORT), int) and DB_PORT is not None and DB_PORT != '':
            #    DB_PORT = input('Please provide us the TCP port on which PostgreSQL is listening. To use the default port, just press. Otherwise input the port: ')
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
        mailware_env_contents = """
            {{
                "debug": false,
                "database": {{
                    "name": "{0}",
                    "user": "{1}",
                    "password": "{2}",
                    "host": "{3}",
                    "port": "{4}",
                    "options": {{
                        "sslmode": "require"
                    }}
                }},
                "language_code": "en-us",
                "time_zone": "{5}",
                "api_only_mode": false,
                "hostconfig": {{
                    "salearn_bin":"{6}",
                    "mailscanner_bin":"{7}",
                    mailscanner_config_dir": "{8}",
                    "mailscanner_share_dir": "{9}",
                    "mailscanner_lib_dir": "{10}",
                    "tmp_dir":"/tmp",
                    "sa_rules_dir":"{11}"
                }},
                "retention": {{
                    "records":{12},
                    "audit":{13},
                    "quarantine":{14}
                }},
                "mta": "{15}"
            }}
        """.format(DB_NAME, DB_USER, DB_PASS, DB_HOST, DB_PORT, TZ, SALEARN_BIN, MS_BIN, MS_CONF_DIR, MS_SHARED, MS_LIB, SA_RULES_DIR, RETENTION_DAYS, RETENTION_DAYS, RETENTION_DAYS, MTA)
        print(mailware_env_contents)
        print('The above is the configuration file that we will save to %s' % '')
        print('After this point everything we do is commited to disk immediately')
        if input('Is this correct and can we continue? (Y/n').lower() == 'n':
            print('Installation will be aborted. Please rerun the installation script to try again')
            exit()
        print('Writing configuration file %s' % APP_DIR + '/mailware-env.json')
        CONF_FILE = open(APP_DIR + '/mailware-env.json', 'w')
        CONF_FILE.write(mailware_env_contents)
        CONF_FILE.close()
        if CONFIGURE_CERTBOT and CONFIGURE_NGINX and CONFIGURE_SYSTEMD:
            if os.geteuid() != 0:
                print('You are not running the installation with root privileges. The script will now terminate')
                exit()
            APP_HOSTNAME = input('Please provide us with the hostname on which your MailWare instance will be accessible [%s]: ' % platform.node())
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
                NGINX_CONF = NGINX_CONF.replace('/home/mailware/cert/domain.tld.crt', CERT_PATH).replace('/home/mailware/cert/domain.tld.key', PRIVKEY_PATH).replace('/home/mailware/cert/dhparam.pem', DHPARAM_PATH)
            else:
                NGINX_CONF = NGINX_CONF.replace('listen 443 ssl http2;', '# listen 443 ssl http2;').replace('if ($scheme = "http") { set $redirect_https 1; }','# if ($scheme = "http") { set $redirect_https 1; }').replace('if ($request_uri ~ ^/.well-known/acme-challenge/) { set $redirect_https 0; }', '# if ($request_uri ~ ^/.well-known/acme-challenge/) { set $redirect_https 0; }').replace('if ($redirect_https) { rewrite ^ https://$server_name$request_uri? permanent; }', '# if ($redirect_https) { rewrite ^ https://$server_name$request_uri? permanent; }').replace('ssl on;','# ssl on;').replace('ssl_certificate /home/mailware/cert/domain.tld.crt;','# ssl_certificate /home/mailware/cert/domain.tld.crt;').replace('ssl_certificate_key /home/mailware/cert/domain.tld.key;','# ssl_certificate_key /home/mailware/cert/domain.tld.key;').replace('ssl_dhparam /home/mailware/cert/dhparam.pem;', '# ssl_dhparam /home/mailware/cert/dhparam.pem;').replace('ssl_session_cache shared:SSL:50m;','# ssl_session_cache shared:SSL:50m;').replace('ssl_session_timeout 30m;','# ssl_session_timeout 30m;').replace('ssl_protocols TLSv1.1 TLSv1.2;','# ssl_protocols TLSv1.1 TLSv1.2;').replace('ssl_ciphers "EECDH+ECDSA+AESGCM EECDH+aRSA+AESGCM EECDH+ECDSA+SHA384 EECDH+ECDSA+SHA256 EECDH+aRSA+SHA384 EECDH+aRSA+SHA256 EECDH+aRSA+RC4 EECDH EDH+aRSA !aNULL !eNULL !LOW !3DES !MD5 !EXP !PSK !SRP !DSS";','# ssl_ciphers "EECDH+ECDSA+AESGCM EECDH+aRSA+AESGCM EECDH+ECDSA+SHA384 EECDH+ECDSA+SHA256 EECDH+aRSA+SHA384 EECDH+aRSA+SHA256 EECDH+aRSA+RC4 EECDH EDH+aRSA !aNULL !eNULL !LOW !3DES !MD5 !EXP !PSK !SRP !DSS";').replace('ssl_prefer_server_ciphers on;','# ssl_prefer_server_ciphers on;')
            NGINX_CONF = NGINX_CONF.replace('domain.tld', APP_HOSTNAME).replace('/home/mailware/app', APP_DIR)
            NGINX_FILE = open(NGINX_PATH + APP_HOSTNAME + NGINX_EXTENSION, 'w')
            NGINX_FILE.write(NGINX_CONF)
            NGINX_FILE.close()
            # Generate systemd service unit file
            SYSTEMD_TMPL = open(APP_DIR + '/examples/systemd/mailware.service', 'r')
            SYSTEMD_UNIT = SYSTEMD_TMPL.read()
            SYSTEMD_UNIT = SYSTEMD_UNIT.replace('/home/mailware/app', APP_DIR).replace('mailware', APP_USER)
            SYSTEMD_FILE = open(SYSTEMD_PATH + 'mailware.service', 'w')
            SYSTEMD_FILE.write(SYSTEMD_UNIT)
            SYSTEMD_FILE.close()
            # Reload systemd unit cache
            os.system(SYSTEMCTL_BIN + ' daemon-reload')
            # Enable systemd service units on startup
            os.system(SYSTEMCTL_BIN + ' enable mailware.service')
            if input('Should we start the MailWare services for you now? (Y/n) ').lower() == 'y':
                # Ask systemd to start mailware.service and mailware-celery.service
                os.system(SYSTEMCTL_BIN + ' start mailware.service')
    print('The installation script has finished. Any errors that occurred during installation need to be fixed manually')
    print('Below is a list of files that we have created during the installation process. If you need to run the installation script again, then you can simply delete these files')
