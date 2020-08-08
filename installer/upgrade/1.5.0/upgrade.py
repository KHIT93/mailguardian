#!/usr/bin/env python3
#
# MailGuardian upgrade script for version 1.5.x
#
import os
import json
from distutils.version import StrictVersion

class Upgrader(object):
    config = []
    app_dir = ''
    src_dir = ''
    version = '1.0.0'
    applied_version = '1.5.0'
    legacy = False

    def __init__(self, config, app_dir='/home/mailguardian/mailguardian', src_dir='/home/mailguardian/mailguardian/src', version='1.0.0'):
        super().__init__()
        self.config = config
        self.app_dir = app_dir
        self.src_dir = src_dir
        self.version = version

    def applicable(self):
        return StrictVersion(self.version) < StrictVersion(self.applied_version)

    def upgrade(self):
        if StrictVersion(self.version) < StrictVersion('1.5.0'):
            env_contents = [
                'from .core_settings import self.src_dir, ASSETS_DIR',
                'import os',
                '# Quick-start production settings',
                '# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/',
                '',
                '# SECURITY WARNING: keep the secret key used in production secret!',
                'SECRET_KEY = "{}"'.format(self.config['app_key']),
                '# SECURITY WARNING: keep the field encryption key used in production secret!',
                '# We use the SECRET_KEY as a fallback for compatibility with existing installations',
                'FIELD_ENCRYPTION_KEY = "{}"'.format(self.config['encryption_key']),
                '',
                'APP_HOSTNAME = "{}"'.format(self.config['hostname']),
                'DEBUG = {}'.format(self.config['debug']),
                'LOCAL_CONFIG_VERSION = "1.5.0"',
                '',
                '#MailGuardian specific settings',
                'TMP_DIR = "/tmp"',
                'MTA = "{}"'.format(self.config['mta']),
                'MTA_LOGFILE = "{}"'.format(self.config['hostconfig']['mta_logfile']),
                'SENDMAIL_BIN = "{}"'.format(self.config['hostconfig']['sendmail_bin']),
                'POSTQUEUE_BIN = "{}"'.format(self.config['hostconfig']['postqueue_bin'] if 'postqueue_bin' in self.config['hostconfig'] else which('postqueue')),
                'AUDIT_LOGGING = {}'.format(self.config['audit_log']),
                'API_ONLY = {}'.format(self.config['api_only_mode']),
                'CONF_DIR = os.path.join(os.path.dirname(self.src_dir), "configuration")',
                '',
                '#MailScanner settings',
                'MAILSCANNER_BIN = "{}"'.format(self.config['hostconfig']['mailscanner_bin']),
                'MAILSCANNER_CONFIG_DIR = "{}"'.format(self.config['hostconfig']['mailscanner_config_dir']),
                'MAILSCANNER_SHARE_DIR = "{}"'.format(self.config['hostconfig']['mailscanner_share_dir']),
                'MAILSCANNER_LIB_DIR = "{}"'.format(self.config['hostconfig']['mailscanner_lib_dir']),
                'MAILSCANNER_QUARANTINE_DIR = "{}"'.format(self.config['hostconfig']['mailscanner_quarantine_dir']),
                '',
                '# SpamAssassin settings',
                'SALEARN_BIN = "{}"'.format(self.config['hostconfig']['salearn_bin']),
                'SA_BIN = "{}"'.format(self.config['hostconfig']['sa_bin']),
                'SA_RULES_DIR = "{}"'.format(self.config['hostconfig']['sa_rules_dir']),
                'SA_PREF = MAILSCANNER_CONFIG_DIR+"/spamassassin.conf"',
                '',
                '# Retention policy',
                'RECORD_RETENTION = {}'.format(self.config['retention']['records']),
                'AUDIT_RETENTION = {}'.format(self.config['retention']['audit']),
                'QUARANTINE_RETENTION = {}'.format(self.config['retention']['quarantine']),
                '',
                '# Branding',
                'BRAND_NAME = "{}"'.format(self.config['branding']['name']),
                'BRAND_TAGLINE = "{}"'.format(self.config['branding']['tagline']),
                'BRAND_LOGO = "{}"'.format(self.config['branding']['logo']),
                '',
                '# Internationalization',
                '# https://docs.djangoproject.com/en/2.2/topics/i18n/',
                'LANGUAGE_CODE = "{}"'.format(self.config['language_code']),
                '',
                'TIME_ZONE = "{}"'.format(self.config['time_zone']),
                '# Database',
                '# https://docs.djangoproject.com/en/2.2/ref/settings/#databases',
                'DATABASES = {',
                '    "default": {',
                '        "ENGINE": "django.db.backends.postgresql",',
                '        "NAME": "{}",'.format(self.config['database']['name']),
                '        "USER": "{}",'.format(self.config['database']['user']),
                '        "PASSWORD": "{}",'.format(self.config['database']['password']),
                '        "HOST": "{}",'.format(self.config['database']['host']),
                '        "PORT": "{}",'.format(self.config['database']['port']),
                '        "OPTIONS": {',
                '            "sslmode": "{}"'.format("require" if self.config['database']['options']['sslmode'] else "prefer"),
                '        },',
                '    }',
                '}'
            ]
            mailguardian_env_contents = "\n".join(env_contents)
            # Write out the new configuration file
            with open(os.path.join(self.src_dir, 'mailguardian','settings', 'local.py'), 'w') as f:
                f.write(mailguardian_env_contents)

            print('We have now migrated the contents of your configuration file into the new format')
            print('Please note that from version 1.5.0 and onwards, a new option for providing a custom support link and user feedback link are available')
            print('Specify the BRAND_SUPPORT and BRAND_FEEDBACK options in {} to take advantage of this'.format(os.path.join(self.src_dir, 'mailguardian','config', 'local.py')))
            print('Deleting old configuration file at {}'.format(os.path.join(self.app_dir, 'mailguardian-env.json')))
            os.remove(os.path.join(self.app_dir, 'mailguardian-env.json'))
