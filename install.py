#!/usr/bin/env python3
#
# MailGuardian installation script
#
import os, sys, platform, pytz, json
from src.core.helpers import which

if __name__ == "__main__":
    print(chr(27) + "[2J")
    # First make sure that we are running on Linux
    if platform.system() != 'Linux':
        print('Your operation system is not supported. MailGuardian can only run on Linux')
        exit()
    # Get the current directory of this script to determine the path to use for hte systemd unit file templates
    APP_DIR = os.path.dirname(os.path.abspath(__file__))

    # Define some paths needed later
    SYSTEMD_PATH = '/lib/systemd/system/'
    NGINX_PATH = None
    NGINX_EXTENSION = ''
    PKG_MGR = None
    OPENSSL_BIN = which('openssl')
    NGINX_BIN = which('nginx')
    SYSTEMCTL_BIN = which('systemctl')

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
    MS_BIN = which('MailScanner')
    MS_LIB = '/usr/lib/MailScanner'
    MS_SHARED = '/usr/share/MailScanner'
    MS_QUARANTINE_DIR = "/var/spool/MailScanner/quarantine"
    SALEARN_BIN = which('salearn')
    SA_BIN = which('spamassassin')
    SA_RULES_DIR = '/var/lib/spamassassin'
    SENDMAIL_BIN = which('sendmail')

    # Detect the Linux distribution
    # If we can detect you specific Linux distribution,
    # we will skip the parts where we configure systemd,
    # and your webserver
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
    print(chr(27) + "[2J")
    if os.geteuid() != 0:
        print('You need to run the installation script as root. Without root elevation, we are unable to configure the system for you')
        print('You can still continue the execution of the installation script, but choose to leave out the parts that require root elevation')
        print(chr(13))
        if input('Do you want to skip steps that require root elevation and allow the script to continue? (y/N) ').lower() == 'y':
            print('We will continue execution but skip the parts that require root elevation')
            CONFIGURE_CERTBOT = False
            CONFIGURE_NGINX = False
            CONFIGURE_SYSTEMD = False
        else:
            print('Please run the script again as root or with sudo, to elevate execution')
            exit()
    print(chr(27) + "[2J")
    print('We will now ask you a series of questions to properly configure the application for you')
    print('Do not worry, as we will not make any changes before all questions have been answered and confirmed by you')

    while True:
        print(chr(27) + "[2J")
        APP_USER_INPUT = input('What is the username of the user running the MailGuardian application? [{0}] '.format(APP_USER))
        if APP_USER_INPUT != '' and APP_USER_INPUT is not None:
            APP_USER = APP_USER_INPUT
            break
        elif APP_USER != '' or APP_USER is not None:
            break

    while True:
        print(chr(27) + "[2J")
        RETENTION_DAYS_INPUT = input('As your system will use quite a bit of space, could you please let us know how many days you want us to keep data in the system? [{0}] '.format(RETENTION_DAYS))
        if RETENTION_DAYS_INPUT != '' and RETENTION_DAYS_INPUT is not None:
            RETENTION_DAYS = RETENTION_DAYS_INPUT
            break
        elif RETENTION_DAYS != '' and RETENTION_DAYS is not None:
            break
    print(chr(27) + "[2J")
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
    while DB_PASS is None:
        DB_PASS = input('Please provide us the password for the PostgreSQL user specified above: ')
        if DB_PASS == '':
            DB_PASS = None
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
    if input('Does you PostgreSQL server support SSL (Y/n) '.lower() == 'n'):
        DB_SSL = False
    # Next we configure the timezone settings
    print(chr(27) + "[2J")
    print('Please provide us with your timezone. This is usually the same as you chose during installation of your operating system. It is usually typed as Region/City. Fx. US/Eastern or Europe/Berlin')
    while True:
        TZ_INPUT = input('Please type in your timezone. To get a list of available timezones type \'?\': ')
        if TZ_INPUT != '' or TZ_INPUT is not None:
            if TZ_INPUT in pytz.all_timezones:
                TZ = TZ_INPUT
                break
    print(chr(27) + "[2J")
    APP_HOSTNAME_INPUT = input('Please provide us with the hostname on which your MailGuardian instance will be accessible [%s]: ' % APP_HOSTNAME)
    if APP_HOSTNAME_INPUT != '' and APP_HOSTNAME_INPUT is not None:
        APP_HOSTNAME = APP_HOSTNAME_INPUT
    
    if input('Would you like to enable HTTP/2 and SSL/TLS (HTTPS) encryption for this instance? (Y/n) ').lower() != 'y':
        HTTP_SECURE = False
    print(chr(27) + "[2J")
    if input('Should this server be part of a configuration that contains multiple servers? (y/N) ').lower() == 'y':
        MULTI_NODE = True
        print(chr(13))
        if input('Is this the server running the webinterface for users and administrators? (y/n) ').lower() == 'y':
            API_ONLY_MODE = False
        else:
            API_ONLY_MODE = True
    else:
        API_ONLY_MODE = False
    print(chr(27) + "[2J")
    if not MULTI_NODE or API_ONLY_MODE:
        print('Available MTA\'s (Mail Transport Agent)')
        print('sendmail')
        print('postfix')
        print('exim')
        MTA_INPUT = input('Which MTA do you want to use? [{0}] '.format(MTA))
        if MTA_INPUT == '' and MTA_INPUT is None:
            MTA = MTA_INPUT
        print(chr(27) + "[2J")
        MS_CONF_DIR_INPUT = input('Where are your MailScanner configuration files located? [{0}] '.format(MS_CONF_DIR))
        if MS_CONF_DIR_INPUT != '' and MS_CONF_DIR_INPUT is not None:
            MS_CONF_DIR = MS_CONF_DIR_INPUT
        print(chr(27) + "[2J")
        MS_BIN_INPUT = input('Please specify the full path to the MailScanner executable file/binary? [{0}] '.format(MS_BIN))
        if MS_BIN_INPUT != '' and MS_BIN_INPUT is not None:
            MS_BIN = MS_BIN_INPUT
        print(chr(27) + "[2J")
        MS_LIB_INPUT = input('Where are the MailScanner application libraries located? [{0}] '.format(MS_LIB))
        if MS_LIB_INPUT != '' and MS_LIB_INPUT is not None:
            MS_LIB = MS_LIB_INPUT
        print(chr(27) + "[2J")
        MS_SHARED_INPUT = input('Please let us know where your MailScanner shared resources are located [{0}] '.format(MS_SHARED))
        if MS_SHARED_INPUT != '' and MS_SHARED_INPUT is not None:
            MS_SHARED = MS_SHARED_INPUT
        print(chr(27) + "[2J")
        SALEARN_BIN_INPUT = input('To correctly handle SPAM, could you please let us know where your \'salearn\' binary is located? [{0}] '.format(SALEARN_BIN))
        if SALEARN_BIN_INPUT != '' and SALEARN_BIN_INPUT is not None:
            SALEARN_BIN = SALEARN_BIN_INPUT
        print(chr(27) + "[2J")
        SA_BIN_INPUT = input('To correctly handle SPAM, could you please let us know where your \'spamassassin\' binary is located? [{0}] '.format(SA_BIN_INPUT))
        if SA_BIN_INPUT != '' and SA_BIN_INPUT is not None:
            SA_BIN = SA_BIN_INPUT
        print(chr(27) + "[2J")
        SA_RULES_DIR_INPUT = input('Please type in the location of your SpamAssassin rules configuration [{0}] '.format(SA_RULES_DIR))
        if SA_RULES_DIR_INPUT != '' and SA_RULES_DIR_INPUT is not None:
            SA_RULES_DIR = SA_RULES_DIR_INPUT
    print(chr(27) + "[2J")
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
            }
        }
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
    mailguardian_env_contents = json.dumps(env_contents)

    # Print the configuration settings
    print('Hostname: {0}'.format(APP_HOSTNAME))
    print('Database name: {0}'.format(DB_NAME))
    print('Database user: {0}'.format(DB_USER))
    print('Database password: {0}'.format(DB_PASS))
    print('Database host: {0}'.format(DB_HOST))
    print('Database TCP port: {0}'.format(DB_PORT))
    print('Use SSL/TLS for database: {0}'.format('Yes' if DB_SSL else 'No'))
    print('Timezone: {0}'.format(TZ))
    if MULTI_NODE and API_ONLY_MODE:
        print('Node type: Multi-node installation (Processing node)')
    elif MULTI_NODE and not API_ONLY_MODE:
        print('Node type: Multi-node installation (Web interface node)')
    else:
        print('Node type: Single-node installation')
    print('Location of \'salearn\' binary: {0}'.format(SALEARN_BIN))
    print('Location of \'spamassassin\' binary: {0}'.format(SA_BIN))
    print('Location of \'MailScanner\' binary: {0}'.format(MS_BIN))
    print('Location of MailScanner configuration files: {0}'.format(MS_CONF_DIR))
    print('Location of MailScanner shared data: {0}'.format(MS_SHARED))
    print('Location of MailScanner shared libraries: {0}'.format(MS_LIB))
    print('Location of SpamAssassin rules: {0}'.format(SA_RULES_DIR))
    print('Location of \'sendmail\' binary: {0}'.format(SENDMAIL_BIN))
    print('Location of the MailScanner Quarantine: {0}'.format(MS_QUARANTINE_DIR))
    print('MTA (Mail Transport Agent): {0}'.format(MTA))
    print('Location of your MTA logfile: {0}'.format(MTA_LOG))
    print('Retention policy: Store for {0} day(s)'.format(RETENTION_DAYS))

    print('The above will be saved in the configuration file that we will located at {0}'.format(os.path.join(APP_DIR, 'mailguardian-env.json')))
    print(chr(13))
    print('After this point everything we do is commited to disk immediately')
    print(chr(13))
    if input('Are the above settings correct and can we continue? (Y/n) ').lower() == 'n':
        print('Installation has been aborted. Please rerun the installation script to try again')
        exit()
    print(chr(27) + "[2J")
    print('Writing configuration file %s' % APP_DIR + '/mailguardian-env.json')
    with open(APP_DIR + '/mailguardian-env.json', 'w') as f:
        f.write(mailguardian_env_contents)
    print(chr(27) + "[2J")
    if CONFIGURE_CERTBOT and CONFIGURE_NGINX and CONFIGURE_SYSTEMD:
        if os.geteuid() != 0:
            print('You are not running the installation with root privileges. The script will now terminate')
            exit()
        if HTTP_SECURE:
            if input('Would you like us to automatically generate a LetsEncrypt certificate for you? (Y/n) ').lower() == 'y':
                print(chr(27) + "[2J")
                # Check if certbot is installed and if not, then we install it
                if not which('certbot'):
                    os.system(PKG_MGR + ' install certbot -y')
                # Request a certificate and note the path
                PRIVKEY_PATH = '/etc/letsencrypt/live/{0}/privkey.pem'.format(APP_HOSTNAME)
                CERT_PATH = '/etc/letsencrypt/live/{0}/fullchain.pem'.format(APP_HOSTNAME)
                os.system(which('certbot') + ' certonly --standalone -d {0} --pre-hook "{1} stop nginx" --post-hook "{1} start nginx"'.format(APP_HOSTNAME, SYSTEMCTL_BIN))
                print('If the certificate was successfully created, please make sure to manually add this cronjob using sudo crontab -e')
                print("0 6,18 * * * python -c 'import random; import time; time.sleep(random.random() * 3600)' && certbot renew")
                print('This will make sure that we try to renew your LetsEncrypt Certificate twice a day and random minutes')
            elif input('Do you want to use an existing certificate? (y/N) ').lower() == 'y':
                print(chr(27) + "[2J")
                PRIVKEY_PATH_INPUT = input('Please provide us the path to your SSL/TLS private key [{0}]: '.format(PRIVKEY_PATH))
                if PRIVKEY_PATH_INPUT != '' or PRIVKEY_PATH_INPUT is not None:
                    PRIVKEY_PATH = PRIVKEY_PATH_INPUT
                print(chr(13))
                CERT_PATH_INPUT = input('Please provide the path for your SSL/TLS certificate [{0}]: '.format(CERT_PATH))
                if CERT_PATH_INPUT != '' or CERT_PATH_INPUT is not None:
                    CERT_PATH = CERT_PATH_INPUT
            else:
                print(chr(27) + "[2J")
                print('Since you did not want us to generate a letsEncrypt Certificate and did not provide us with a Certificate from a trusted Certification Authority, we will generate a self-signed certificate')
                # Generate a new 4096-bit private key and CSR (Certificate Signing Request)
                os.system(OPENSSL_BIN + ' req -new -newkey rsa:4096 -nodes -keyout {0} -out {1}'.format(PRIVKEY_PATH, CSR_PATH))
            print(chr(27) + "[2J")
            print('Now that we have all the details for your SSL/TLS Certificate, we will generate a set of parameters needed to improve security of the encryption')
            print('Please note that this step can take up to 30 minutes to complete')
            os.system(OPENSSL_BIN + ' dhparam -out {0} 4096'.format(DHPARAM_PATH))
        # Store the nginx configuration file for the application
        with open(os.path.join(APP_DIR, '/examples/nginx/domain.tld'), 'r') as t:
            conf = t.read()
            if HTTP_SECURE:
                conf = conf.replace('/home/mailguardian/cert/domain.tld.crt', CERT_PATH).replace('/home/mailguardian/cert/domain.tld.key', PRIVKEY_PATH).replace('/home/mailguardian/cert/dhparam.pem', DHPARAM_PATH)
            else:
                conf = conf.replace('listen 443 ssl http2;', '# listen 443 ssl http2;').replace('if ($scheme = "http") { set $redirect_https 1; }','# if ($scheme = "http") { set $redirect_https 1; }').replace('if ($request_uri ~ ^/.well-known/acme-challenge/) { set $redirect_https 0; }', '# if ($request_uri ~ ^/.well-known/acme-challenge/) { set $redirect_https 0; }').replace('if ($redirect_https) { rewrite ^ https://$server_name$request_uri? permanent; }', '# if ($redirect_https) { rewrite ^ https://$server_name$request_uri? permanent; }').replace('ssl on;','# ssl on;').replace('ssl_certificate /home/mailguardian/cert/domain.tld.crt;','# ssl_certificate /home/mailguardian/cert/domain.tld.crt;').replace('ssl_certificate_key /home/mailguardian/cert/domain.tld.key;','# ssl_certificate_key /home/mailguardian/cert/domain.tld.key;').replace('ssl_dhparam /home/mailguardian/cert/dhparam.pem;', '# ssl_dhparam /home/mailguardian/cert/dhparam.pem;').replace('ssl_session_cache shared:SSL:50m;','# ssl_session_cache shared:SSL:50m;').replace('ssl_session_timeout 30m;','# ssl_session_timeout 30m;').replace('ssl_protocols TLSv1.1 TLSv1.2;','# ssl_protocols TLSv1.1 TLSv1.2;').replace('ssl_ciphers "EECDH+ECDSA+AESGCM EECDH+aRSA+AESGCM EECDH+ECDSA+SHA384 EECDH+ECDSA+SHA256 EECDH+aRSA+SHA384 EECDH+aRSA+SHA256 EECDH+aRSA+RC4 EECDH EDH+aRSA !aNULL !eNULL !LOW !3DES !MD5 !EXP !PSK !SRP !DSS";','# ssl_ciphers "EECDH+ECDSA+AESGCM EECDH+aRSA+AESGCM EECDH+ECDSA+SHA384 EECDH+ECDSA+SHA256 EECDH+aRSA+SHA384 EECDH+aRSA+SHA256 EECDH+aRSA+RC4 EECDH EDH+aRSA !aNULL !eNULL !LOW !3DES !MD5 !EXP !PSK !SRP !DSS";').replace('ssl_prefer_server_ciphers on;','# ssl_prefer_server_ciphers on;')
            with open(os.path.join(NGINX_PATH, APP_HOSTNAME + NGINX_EXTENSION), 'w') as f:
                f.write(conf)

        # Store the systemd unit file
        with open(os.path.join(APP_DIR, '/examples/systemd/mailguardian.service'), 'r') as t:
            conf = t.read()
            conf = conf.replace('/home/mailguardian/app', APP_DIR).replace('mailguardian', APP_USER)
            with open(os.path.join(SYSTEMD_PATH, 'mailguardian.service'), 'w') as f:
                f.write(conf)

        # Reload systemd unit cache
        os.system(SYSTEMCTL_BIN + ' daemon-reload')

        # Enable systemd service unit on startup
        os.system(SYSTEMCTL_BIN + ' enable mailguardian.service')
        print(chr(27) + "[2J")
        if input('Should we start the MailGuardian services for you now? (Y/n) ').lower() == 'y':
            os.system(SYSTEMCTL_BIN + ' start mailguardian.service')
    print(chr(27) + "[2J")
    print('The installation script has finished. Any errors that occurred during installation need to be fixed manually')
    print('You can now access MailGuardian and perform the last steps of the setup here: {0}://{1}'.format('https' if HTTP_SECURE else 'http', APP_HOSTNAME))
