#!/usr/bin/env python3
#
# MailGuardian upgrade script for version 1.3.x
#
import os
import json
from distutils.version import StrictVersion
from ..tools import Upgrader as BaseUpgrader

class Upgrader(BaseUpgrader):
    applied_version = '2.0.0'
    def upgrade(self):
        if StrictVersion(self.version) >= StrictVersion('1.5.0'):
            print('Unable to upgrade MailGuardian to {version} as it is required to be at version 1.5.0 first'.format(version=self.applied_version))
            return False
        if StrictVersion(self.version) < StrictVersion('2.0.0'):
            pass
    def applicable(self):
        return StrictVersion(self.version) < StrictVersion(self.applied_version) and StrictVersion(self.version) >= StrictVersion('1.5.0')
