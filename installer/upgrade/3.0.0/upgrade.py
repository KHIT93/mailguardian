#!/usr/bin/env python3
#
# MailGuardian upgrade script for version 3.x.x
#
import subprocess
import sys
import os
import json
from distutils.version import StrictVersion
import cryptography.fernet

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
        subprocess.check_call([sys.executable, "-m", "pip", "uninstall", 'django-rest-auth coreschema chardet psycopg2', '-y'])
        self.notices.append('As part of a larger cleaning of dependencies, we have removed the following packages: django-rest-auth coreschema chardet psycopg2')
        self.notices.append('Unless you for some reason have added other tools on top of MailGuardian, you can safely ignore the above')
    def applicable(self):
        return StrictVersion(self.version) < StrictVersion(self.applied_version)