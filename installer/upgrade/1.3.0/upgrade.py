#!/usr/bin/env python3
#
# MailGuardian upgrade script for version 1.3.x
#
import os
import json
from distutils.version import StrictVersion

class Upgrader(object):
    config = []
    app_dir = ''
    src_dir = ''
    version = '1.0.0'
    applied_version = '1.3.0'
    legacy = True
    
    def __init__(self, config, app_dir='/home/mailguardian/mailguardian', src_dir='/home/mailguardian/mailguardian/src', version='1.0.0'):
        super().__init__()
        self.config = config
        self.app_dir = app_dir
        self.src_dir = src_dir
        self.version = version
    
    def upgrade(self):
        if StrictVersion(self.version) < StrictVersion('1.3.0'):
            self.config['encryption_key'] = self._generate_encryption_key()
            with open(os.path.join(app_dir, 'mailguardian-env.json'), 'w') as f:
                f.write(json.dumps(self.config))
            return True
        else:
            return False
    
    def applicable(self):
        return StrictVersion(self.version) < StrictVersion(self.applied_version)
    
    def _generate_encryption_key(self):
        key = cryptography.fernet.Fernet.generate_key()
        return key.decode()
