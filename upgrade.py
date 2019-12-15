#!/usr/bin/env python3
#
# MailGuardian upgrade script
#
from django.core.management.utils import get_random_secret_key
from src.core.helpers import which
import os, json, platform
from distutils.version import StrictVersion
import cryptography.fernet
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-y','--yes', help='Answer yes to every question and perform update with no interaction', action="store_true")

args = parser.parse_args()

def generate_encryption_key():
    key = cryptography.fernet.Fernet.generate_key()
    return key.decode()

def rebuild_latest_nginx():
    pass

def rebuild_latest_systemd():
    pass

if __name__ == "__main__":
    os.system('clear')
    # First make sure that we are running on Linux
    if platform.system() != 'Linux':
        print('Your operation system is not supported. MailGuardian can only run on Linux')
        exit()
    # Get the current directory of this script to determine the path to use
    APP_DIR = os.path.dirname(os.path.abspath(__file__))
    BASE_DIR = os.path.join(APP_DIR,'src')
    if input('This script will evaluate your curren MailGuardian installation and apply any changes necessary. Do you want to start? (y/N) ').lower() != 'y':
        exit(0)
    os.system('clear')
    if os.path.exists(os.path.join(APP_DIR, 'mailguardian-env.json')):
        print('Configuration file prior to version 1.5.0 has been detected')
        print('COnfiguration file will be converted to new format')
        CONFIG = {}
        with open(os.path.join(APP_DIR, 'mailguardian-env.json'), 'r') as f:
            CONFIG = json.loads(f.read())
        # Check if config_version is available in CONFIG
        if not 'config_version' in CONFIG:
            # If not there, then we asume a version prior to 1.3.0
            CONFIG_VERSION = '1.0.0'
        else:
            CONFIG_VERSION = CONFIG['config_version']
        # Check if we are below 1.3.0
        if StrictVersion(CONFIG_VERSION) < StrictVersion('1.3.0'):
            if not 'encryption_key' in CONFIG:
                CONFIG['encryption_key'] = generate_encryption_key()
        print('Generating new configuration file')
        env_contents = [
            'from .core_settings import BASE_DIR, ASSETS_DIR',
            'import os',
            '# Quick-start development settings - unsuitable for production',
            '# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/',
            '',
            '# SECURITY WARNING: keep the secret key used in production secret!',
            'SECRET_KEY = "{}"'.format(CONFIG['app_key']),
            '# SECURITY WARNING: keep the field encryption key used in production secret!',
            '# We use the SECRET_KEY as a fallback for compatibility with existing installations',
            'FIELD_ENCRYPTION_KEY = "{}"'.format(CONFIG['encryption_key']),
            '',
            'APP_HOSTNAME = "{}"'.format(CONFIG['hostname']),
            'DEBUG = {}'.format(CONFIG['debug']),
            'LOCAL_CONFIG_VERSION = "1.5.0"',
            '',
            '#MailGuardian specific settings',
            'TMP_DIR = "/tmp"',
            'MTA = "{}"'.format(CONFIG['mta']),
            'MTA_LOGFILE = "{}"'.format(CONFIG['hostconfig']['mta_logfile']),
            'SENDMAIL_BIN = "{}"'.format(CONFIG['hostconfig']['sendmail_bin']),
            'POSTQUEUE_BIN = "{}"'.format(CONFIG['hostconfig']['postqueue_bin'] if 'postqueue_bin' in CONFIG['hostconfig'] else which('postqueue')),
            'AUDIT_LOGGING = {}'.format(CONFIG['audit_log']),
            'API_ONLY = {}'.format(CONFIG['api_only_mode']),
            'CONF_DIR = os.path.join(os.path.dirname(BASE_DIR), "configuration")',
            '',
            '#MailScanner settings',
            'MAILSCANNER_BIN = "{}"'.format(CONFIG['hostconfig']['mailscanner_bin']),
            'MAILSCANNER_CONFIG_DIR = "{}"'.format(CONFIG['hostconfig']['mailscanner_config_dir']),
            'MAILSCANNER_SHARE_DIR = "{}"'.format(CONFIG['hostconfig']['mailscanner_share_dir']),
            'MAILSCANNER_LIB_DIR = "{}"'.format(CONFIG['hostconfig']['mailscanner_lib_dir']),
            'MAILSCANNER_QUARANTINE_DIR = "{}"'.format(CONFIG['hostconfig']['mailscanner_quarantine_dir']),
            '',
            '# SpamAssassin settings',
            'SALEARN_BIN = "{}"'.format(CONFIG['hostconfig']['salearn_bin']),
            'SA_BIN = "{}"'.format(CONFIG['hostconfig']['sa_bin']),
            'SA_RULES_DIR = "{}"'.format(CONFIG['hostconfig']['sa_rules_dir']),
            'SA_PREF = MAILSCANNER_CONFIG_DIR+"/spamassassin.conf"',
            '',
            '# Retention policy',
            'RECORD_RETENTION = {}'.format(CONFIG['retention']['records']),
            'AUDIT_RETENTION = {}'.format(CONFIG['retention']['audit']),
            'QUARANTINE_RETENTION = {}'.format(CONFIG['retention']['quarantine']),
            '',
            '# Branding',
            'BRAND_NAME = "{}"'.format(CONFIG['branding']['name']),
            'BRAND_TAGLINE = "{}"'.format(CONFIG['branding']['tagline']),
            'BRAND_LOGO = "{}"'.format(CONFIG['branding']['logo']),
            '',
            '# Internationalization',
            '# https://docs.djangoproject.com/en/2.2/topics/i18n/',
            'LANGUAGE_CODE = "{}"'.format(CONFIG['language_code']),
            '',
            'TIME_ZONE = "{}"'.format(CONFIG['time_zone']),
            '# Database',
            '# https://docs.djangoproject.com/en/2.2/ref/settings/#databases',
            'DATABASES = {',
            '    "default": {',
            '        "ENGINE": "django.db.backends.postgresql",',
            '        "NAME": "{}",'.format(CONFIG['database']['name']),
            '        "USER": "{}",'.format(CONFIG['database']['user']),
            '        "PASSWORD": "{}",'.format(CONFIG['database']['password']),
            '        "HOST": "{}",'.format(CONFIG['database']['host']),
            '        "PORT": "{}",'.format(CONFIG['database']['port']),
            '        "OPTIONS": {',
            '            "sslmode": "{}"'.format("require" if CONFIG['database']['options']['sslmode'] else "prefer"),
            '        },',
            '    }',
            '}'
        ]
        mailguardian_env_contents = "\n".join(env_contents)
        # Write out the new configuration file
        with open(os.path.join(BASE_DIR, 'mailguardian','config', 'local.py'), 'w') as f:
            f.write(mailguardian_env_contents)

        print('We have now migrated the contents of your configuration file into the new format')
        print('Please note that from version 1.5.0 and onwards, a new option for providing a custom support link and user feedback link are available')
        print('Specify the BRAND_SUPPORT and BRAND_FEEDBACK options in {} to take advantage of this'.format(os.path.join(BASE_DIR, 'mailguardian','config', 'local.py')))
        print('Deleting old configuration file at {}'.format(os.path.join(APP_DIR, 'mailguardian-env.json')))
        os.remove(os.path.join(APP_DIR, 'mailguardian-env.json'))
        print('Old configuration data removed. Now we will perform remaining upgrade tasks')

    print('Performing upgrade tasks for version 1.5.0')

    print('Now we will perform actions that need to be performed after any file changes')

    # Apply changes that require configuration file changes to have been persisted
    os.system('{0} src/manage.py migrate'.format(which('python')))
    if os.path.exists(os.path.join(APP_DIR, 'mix-manifest.json')) and which('npm'):
        # If we run the frontend, then we will have to perform node updates
        print('Web frontend detected. Rebuilding static assets. This may take some time')
        os.system('npm install')
        os.system('npm run production')
    auto_fix = args.yes

    if not auto_fix:
        if input('Do you want us to automatically migrate your Nginx configuration to match our latest template (y/N) ').lower() == 'y':
            auto_fix = True
    
    if auto_fix:
        rebuild_latest_nginx()
        auto_fix = False
    
    if not auto_fix:
        if input('Do you want us to automatically migrate your Systemd service configuration to match our latest template (y/N) ').lower() == 'y':
            auto_fix = True
    
    if auto_fix:
        rebuild_latest_systemd()
        auto_fix = False
    