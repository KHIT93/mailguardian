#!/usr/bin/env python3
#
# MailGuardian upgrade script for version 3.0.0
#
from distutils.version import StrictVersion
import subprocess

class Upgrader(object):
    config = []
    app_dir = ''
    src_dir = ''
    version = '1.0.0'
    applied_version = '3.0.0'
    legacy = False
    notices = []

    def __init__(self, config, app_dir='/home/mailguardian/mailguardian', src_dir='/home/mailguardian/mailguardian/src', version='1.0.0'):
        super().__init__()
        self.config = config
        self.app_dir = app_dir
        self.src_dir = src_dir
        self.version = version
    def upgrade(self):
        if StrictVersion(self.version) <= StrictVersion('1.5.0'):
            print('Current version detected as {version}'.format(version=self.version))
            print('Unable to upgrade MailGuardian to {version} as it is required to be at version 1.5.0 first'.format(version=self.applied_version))
            return False
        if StrictVersion(self.version) < StrictVersion('3.0.0'):
            subprocess.call('pip uninstall django-rest-auth django-premailer pytz chardet coreschema Jinja2 MarkupSafe  -y', shell=True)
            return True
    def applicable(self):
        return StrictVersion(self.version) < StrictVersion(self.applied_version) and StrictVersion(self.version) >= StrictVersion('1.5.0')