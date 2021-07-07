#!/usr/bin/env python3
#
# MailGuardian installation script
#
import os, sys, platform, pytz, json, pwd, grp, subprocess
from django.core.management.utils import get_random_secret_key
import configparser
import argparse
import distro as distribution
import cryptography.fernet

parser = argparse.ArgumentParser()
parser.add_argument('-f','--config-file', help='Input path to environment configuration file')

args = parser.parse_args()

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
    return False

def generate_encryption_key():
    key = cryptography.fernet.Fernet.generate_key()
    return key.decode()


if __name__ == "__main__":
    os.system('clear')
    # First make sure that we are running on Linux
    if platform.system() != 'Linux':
        print('Your operation system is not supported. MailGuardian can only run on Linux')
        exit(255)
    installer_config = configparser.ConfigParser()
    installer_config.read(args.config_file)
    # Get the current directory of this script to determine the path to use for the systemd unit file templates
    APP_DIR  = installer_config['mailguardian']['app_dir']
    c
    # Define some paths needed later
    SYSTEMD_PATH = '/etc/systemd/system/'
    NGINX_PATH = installer_config['nginx']['path']
    NGINX_EXTENSION = installer_config['nginx']['extension'] or ''
    PKG_MGR = installer_config['bin']['pkg']
    OPENSSL_BIN = installer_config['bin']['openssl']
    NGINX_BIN = installer_config['bin']['nginx']
    SYSTEMCTL_BIN = installer_config['bin']['systemctl']

    # Define some variables to store whether we need to skip some steps
    CONFIGURE_NGINX = installer_config['installation'].getboolean('nginx')
    CONFIGURE_SYSTEMD = installer_config['installation'].getboolean('systemd')
    CONFIGURE_CERTBOT = installer_config['installation'].getboolean('certbot')
    HTTP_SECURE = installer_config['mailguardian'].getboolean('https')

    # Define variables to store generic data for use regardless of the installation purpose
    APP_HOSTNAME = installer_config['mailguardian']['hostname']
    APP_USER = installer_config['mailguardian']['user']
    if not installer_config['mailguardian']['secret']:
        installer_config['mailguardian']['secret'] = get_random_secret_key()
    APP_SECRET = installer_config['mailguardian']['secret']
    RETENTION_DAYS = installer_config['mailguardian']['retention']
    DB_HOST = installer_config['database']['host']
    DB_USER = installer_config['database']['user']
    DB_PASS = installer_config['database']['pass']
    DB_NAME = installer_config['database']['name']
    DB_PORT = installer_config['database']['port']
    DB_SSL = installer_config['database']['ssl']
    TZ = installer_config['mailguardian']['tz']
    PRIVKEY_PATH = installer_config['installation']['privkey']
    CSR_PATH = installer_config['installation']['csr']
    CERT_PATH = installer_config['installation']['cert']
    DHPARAM_PATH = installer_config['installation']['dhparam']

    # Stuff related to mulit-node configurations
    MULTI_NODE = installer_config['mailguardian'].getboolean('multi_node')
    API_ONLY_MODE = installer_config['mailguardian'].getboolean('api_only')

    # Define some variables to use for processing nodes
    # These will be relevant for a single-node deployment,
    # as well as a multi-node deployment
    MTA = installer_config['mailguardian']['mta']
    MTA_LOG = installer_config['mailguardian']['mta_log']
    MS_CONF_DIR = installer_config['mailscanner']['config']
    MS_BIN = installer_config['mailscanner']['bin']
    MS_LIB = installer_config['mailscanner']['lib']
    MS_SHARED = installer_config['mailscanner']['shared']
    MS_QUARANTINE_DIR = installer_config['mailscanner']['quarantine']
    SALEARN_BIN = installer_config['spamassassin']['sa_learn']
    SA_BIN = installer_config['spamassassin']['bin']
    SA_RULES_DIR = installer_config['spamassassin']['rules']
    SENDMAIL_BIN = installer_config['mailscanner']['sendmail']
    POSTQUEUE_BIN = installer_config['mailscanner']['postqueue']

    with open(args.config_file, 'w') as f:
        installer_config.write(f)
    # Detect the Linux distribution
    # If we can detect you specific Linux distribution,
    # we will skip the parts where we configure systemd,
    # and your webserver
    distro_data = distribution.linux_distribution(full_distribution_name=False)
    distro = distro_data[0] or 'LINUX'
    distro_version = distro_data[1] or '0'
    distro_version_codename = distro_data[2] or 'Core'
    if distro.lower() not in ['centos', 'debian', 'ubuntu']:
        print('Your Linux distribution or version is not supported')
        print(distro)
        exit(255)

    os.system('clear')

    env_contents = [
        'import os',
        'from .core_settings import BASE_DIR',
        '# Quick-start production settings',
        '# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/',
        '',
        '# SECURITY WARNING: keep the secret key used in production secret!',
        'SECRET_KEY = "{}"'.format(APP_SECRET),
        '',
        'APP_HOSTNAME = "{}"'.format(APP_HOSTNAME),
        'DEBUG = False',
        'LOCAL_CONFIG_VERSION = "2.0.0"',
        '',
        '#MailGuardian specific settings',
        'TMP_DIR = "/tmp"',
        'MTA = "{}"'.format(MTA),
        'MTA_LOGFILE = "{}"'.format(MTA_LOG),
        'SENDMAIL_BIN = "{}"'.format(SENDMAIL_BIN),
        'POSTQUEUE_BIN = "{}"'.format(POSTQUEUE_BIN),
        'AUDIT_LOGGING = True',
        'API_ONLY = {}'.format(API_ONLY_MODE),
        'CONF_DIR = os.path.join(os.path.dirname(BASE_DIR), "configuration")',
        '',
        '#MailScanner settings',
        'MAILSCANNER_BIN = "{}"'.format(MS_BIN),
        'MAILSCANNER_CONFIG_DIR = "{}"'.format(MS_CONF_DIR),
        'MAILSCANNER_SHARE_DIR = "{}"'.format(MS_SHARED),
        'MAILSCANNER_LIB_DIR = "{}"'.format(MS_LIB),
        'MAILSCANNER_QUARANTINE_DIR = "{}"'.format(MS_QUARANTINE_DIR),
        '',
        '# SpamAssassin settings',
        'SALEARN_BIN = "{}"'.format(SALEARN_BIN),
        'SA_BIN = "{}"'.format(SA_BIN),
        'SA_RULES_DIR = "{}"'.format(SA_RULES_DIR),
        'SA_PREF = MAILSCANNER_CONFIG_DIR+"/spamassassin.conf"',
        '',
        '# Retention policy',
        'RECORD_RETENTION = {}'.format(RETENTION_DAYS),
        'AUDIT_RETENTION = {}'.format(RETENTION_DAYS),
        'QUARANTINE_RETENTION = {}'.format(RETENTION_DAYS),
        '',
        '# Branding',
        'BRAND_NAME = "MailGuardian"',
        'BRAND_TAGLINE = "Securing your email"',
        'BRAND_LOGO = ""',
        '',
        '# Internationalization',
        '# https://docs.djangoproject.com/en/3.1/topics/i18n/',
        'LANGUAGE_CODE = "en-us"',
        '',
        'TIME_ZONE = "{}"'.format(TZ),
        '# Database',
        '# https://docs.djangoproject.com/en/3.1/ref/settings/#databases',
        'DATABASES = {',
        '    "default": {',
        '        "ENGINE": "django.db.backends.postgresql",',
        '        "NAME": "{}",'.format(DB_NAME),
        '        "USER": "{}",'.format(DB_USER),
        '        "PASSWORD": "{}",'.format(DB_PASS),
        '        "HOST": "{}",'.format(DB_HOST),
        '        "PORT": "{}",'.format(DB_PORT),
        '        "OPTIONS": {',
        '            "sslmode": "{}"'.format("require" if DB_SSL else "prefer"),
        '        },',
        '    }',
        '}'
    ]
    mailguardian_env_contents = "\n".join(env_contents)
    print('Writing configuration file {0}'.format(os.path.join(APP_DIR, 'src', 'mailguardian', 'settings', 'local.py')))
    with open(os.path.join(APP_DIR, 'src', 'mailguardian', 'settings', 'local.py'), 'w') as f:
        f.write(mailguardian_env_contents)
    os.chown(os.path.join(APP_DIR, 'src', 'mailguardian', 'settings', 'local.py'), pwd.getpwnam(APP_USER).pw_uid, grp.getgrnam(APP_USER).gr_gid)
    os.system('clear')
    if CONFIGURE_CERTBOT and CONFIGURE_NGINX and CONFIGURE_SYSTEMD:
        if os.geteuid() != 0:
            print('You are not running the installation with root privileges. The script will now terminate')
            exit()
        if HTTP_SECURE:
            if installer_config['installation'].getboolean('letsencrypt'):
                # Check if certbot is installed and if not, then we install it
                if not which('certbot'):
                    if distro == 'debian':
                        os.system(PKG_MGR + ' install certbot -t {distro}-backports -y'.format(distro=distro_version_codename))
                    else:
                        os.system(PKG_MGR + ' install certbot -y')
                # Request a certificate and note the path
                PRIVKEY_PATH = '/etc/letsencrypt/live/{0}/privkey.pem'.format(APP_HOSTNAME)
                CERT_PATH = '/etc/letsencrypt/live/{0}/fullchain.pem'.format(APP_HOSTNAME)
                os.system(which('certbot') + ' certonly --standalone --rsa-key-size 4096 -d {0} --pre-hook "{1} stop nginx" --post-hook "{1} start nginx"'.format(APP_HOSTNAME, SYSTEMCTL_BIN))
            else:
                print('Since you did not want us to generate a letsEncrypt Certificate and did not provide us with a Certificate from a trusted Certification Authority, we will generate a self-signed certificate')
                # Generate a new 4096-bit private key and CSR (Certificate Signing Request)
                os.system(OPENSSL_BIN + ' req -new -newkey rsa:4096 -nodes -keyout {0} -out {1}'.format(PRIVKEY_PATH, CSR_PATH))
                os.chown(PRIVKEY_PATH, pwd.getpwnam(APP_USER).pw_uid, grp.getgrnam(APP_USER).gr_gid)
                os.chown(CSR_PATH, pwd.getpwnam(APP_USER).pw_uid, grp.getgrnam(APP_USER).gr_gid)
                os.system(OPENSSL_BIN + ' x509 -req -days 3650 -in {csr} -signkey {key} -out {crt}'.format(csr=CSR_PATH, key=PRIVKEY_PATH, crt=CERT_PATH))
                os.chown(CERT_PATH, pwd.getpwnam(APP_USER).pw_uid, grp.getgrnam(APP_USER).gr_gid)
            print('Now that we have all the details for your SSL/TLS Certificate, we will generate a set of parameters needed to improve security of the encryption')
            print('Please note that this step can take up to 30 minutes to complete')
            os.system(OPENSSL_BIN + ' dhparam -out {0} 4096'.format(DHPARAM_PATH))
            os.chown(DHPARAM_PATH, pwd.getpwnam(APP_USER).pw_uid, grp.getgrnam(APP_USER).gr_gid)
        # Store the nginx configuration file for the application
        with open(os.path.join(APP_DIR, 'configuration', 'examples','nginx','domain.tld'), 'r') as t:
            conf = t.read()
            if HTTP_SECURE:
                conf = conf.replace('/home/mailguardian/cert/domain.tld.crt', CERT_PATH).replace('/home/mailguardian/cert/domain.tld.key', PRIVKEY_PATH).replace('/home/mailguardian/cert/dhparam.pem', DHPARAM_PATH)
            else:
                conf = conf.replace('listen 443 ssl http2;', '# listen 443 ssl http2;').replace('if ($scheme = "http") { set $redirect_https 1; }','# if ($scheme = "http") { set $redirect_https 1; }').replace('if ($request_uri ~ ^/.well-known/acme-challenge/) { set $redirect_https 0; }', '# if ($request_uri ~ ^/.well-known/acme-challenge/) { set $redirect_https 0; }').replace('if ($redirect_https) { rewrite ^ https://$server_name$request_uri? permanent; }', '# if ($redirect_https) { rewrite ^ https://$server_name$request_uri? permanent; }').replace('ssl on;','# ssl on;').replace('ssl_certificate /home/mailguardian/cert/domain.tld.crt;','# ssl_certificate /home/mailguardian/cert/domain.tld.crt;').replace('ssl_certificate_key /home/mailguardian/cert/domain.tld.key;','# ssl_certificate_key /home/mailguardian/cert/domain.tld.key;').replace('ssl_dhparam /home/mailguardian/cert/dhparam.pem;', '# ssl_dhparam /home/mailguardian/cert/dhparam.pem;').replace('ssl_session_cache shared:SSL:50m;','# ssl_session_cache shared:SSL:50m;').replace('ssl_session_timeout 30m;','# ssl_session_timeout 30m;').replace('ssl_protocols TLSv1.1 TLSv1.2;','# ssl_protocols TLSv1.1 TLSv1.2;').replace('ssl_ciphers "EECDH+ECDSA+AESGCM EECDH+aRSA+AESGCM EECDH+ECDSA+SHA384 EECDH+ECDSA+SHA256 EECDH+aRSA+SHA384 EECDH+aRSA+SHA256 EECDH+aRSA+RC4 EECDH EDH+aRSA !aNULL !eNULL !LOW !3DES !MD5 !EXP !PSK !SRP !DSS";','# ssl_ciphers "EECDH+ECDSA+AESGCM EECDH+aRSA+AESGCM EECDH+ECDSA+SHA384 EECDH+ECDSA+SHA256 EECDH+aRSA+SHA384 EECDH+aRSA+SHA256 EECDH+aRSA+RC4 EECDH EDH+aRSA !aNULL !eNULL !LOW !3DES !MD5 !EXP !PSK !SRP !DSS";').replace('ssl_prefer_server_ciphers on;','# ssl_prefer_server_ciphers on;')
            conf = conf.replace('server_name domain.tld;', 'server_name {0};'.format(APP_HOSTNAME)).replace('access_log /var/log/nginx/domain.tld.access.log;', 'access_log /var/log/nginx/{0}.access.log;'.format(APP_HOSTNAME)).replace('error_log /var/log/nginx/domain.tld.error.log;', 'error_log /var/log/nginx/{0}.error.log;'.format(APP_HOSTNAME))
            if distro == 'centos':
                if distro_version == '8':
                    conf.replace('include proxy_params;', '#include proxy_params;')
            with open(os.path.join(NGINX_PATH, APP_HOSTNAME + NGINX_EXTENSION), 'w') as f:
                f.write(conf)

        # Store the systemd socket file
        with open(os.path.join(APP_DIR, 'configuration', 'examples','systemd','mailguardian.socket'), 'r') as t:
            conf = t.read()
            with open(os.path.join(SYSTEMD_PATH, 'mailguardian.socket'), 'w') as f:
                f.write(conf)

        # Store the systemd unit file
        with open(os.path.join(APP_DIR, 'configuration', 'examples','systemd','mailguardian.service'), 'r') as t:
            conf = t.read()
            conf = conf.replace('/home/mailguardian/mailguardian', APP_DIR).replace('mailguardian', APP_USER)
            with open(os.path.join(SYSTEMD_PATH, 'mailguardian.service'), 'w') as f:
                f.write(conf)
        os.system('mkdir -p {0}'.format(os.path.join('var', 'log', 'mailguardian')))
        os.system('touch {0}'.format(os.path.join('var', 'log', 'mailguardian', 'app.log')))
        os.system('chown 777 {}:{}'.format(APP_USER, 'mtagroup'))
        # Reload systemd unit cache
        os.system(SYSTEMCTL_BIN + ' daemon-reload')

        # Enable systemd service unit on startup
        os.system(SYSTEMCTL_BIN + ' enable --now mailguardian.service')
