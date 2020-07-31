#!/usr/bin/env python3
#
# MailGuardian upgrade script for version 1.3.x
#
import os
import json
from distutils.version import StrictVersion
from ..tools import Upgrader as BaseUpgrader

class Upgrader(BaseUpgrader):
    applied_version = '1.3.0'
    legacy = True
    def upgrade(self):
        if StrictVersion(self.version) < StrictVersion('1.3.0'):
            self.config['encryption_key'] = self._generate_encryption_key()
            with open(os.path.join(app_dir, 'mailguardian-env.json'), 'w') as f:
                f.write(json.dumps(self.config))
