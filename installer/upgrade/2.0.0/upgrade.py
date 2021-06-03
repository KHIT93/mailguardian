#!/usr/bin/env python3
#
# MailGuardian upgrade script for version 1.3.x
#
import os
import json
from distutils.version import StrictVersion
import cryptography.fernet

class Upgrader(object):
    config = []
    app_dir = ''
    src_dir = ''
    version = '1.0.0'
    applied_version = '2.0.0'
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
        if StrictVersion(self.version) < StrictVersion('2.0.0'):
            self.notices.append('From 2.0.0 and going forward, we will use the Postfix Milter implementation of MailScanner. If you are currently using the 1.x.x configuration using plain Postfix, it is also okay, as it will still be supported')
            self.notices.append('You can migrate to the filter by running the milter-migration.py file inside the {app_dir}/installer/tools folder as root. This will change over to using the Milter'.format(app_dir=self.app_dir))
            self.notices.append('From 2.0.0 and onwards, we use GeoIP data using the GeoLite2 databases from MaxMind. To configure this, you need to add the MAXMIND_ACCOUNT_API_KEY to your settings. See https://mailguardian.org/docs/')
            return True
    def applicable(self):
        return StrictVersion(self.version) < StrictVersion(self.applied_version) and StrictVersion(self.version) >= StrictVersion('1.5.0')