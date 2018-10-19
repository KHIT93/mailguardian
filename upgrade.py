#!/usr/bin/env python3
#
# MailGuardian installation script
#
from django.core.management.utils import get_random_secret_key
from src.mailguardian.settings import APP_VERSION
from src.core.helpers import which
import cryptography.fernet
import os, json
from distutils.version import StrictVersion

def generate_encryption_key():
    key = cryptography.fernet.Fernet.generate_key()
    return key.decode()

if __name__ == "__main__":
    os.system('clear')
    # First make sure that we are running on Linux
    if platform.system() != 'Linux':
        print('Your operation system is not supported. MailGuardian can only run on Linux')
        exit()
    # Get the current directory of this script to determine the path to use
    APP_DIR = os.path.dirname(os.path.abspath(__file__))
    if input('This script will evaluate your curren MailGuardian installation and apply any changes necessary. Do you want to start? (y/N) ').lower() != 'y':
        print('Please relaunch this script after running \'pip install -r requirements.txt\' ')
        exit()
    os.system('clear')
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
    # Apply other changes to configuration files

    # Persist configuration file changes to disk
    CONFIG['config_version'] = APP_VERSION
    with open(os.path.join(APP_DIR, 'mailguardian-env.json'), 'w') as f:
        f.write(json.dumps(CONFIG))

    # Apply changes that require configuration file changes to have been persisted
    os.system('{0} src/manage.py migrate'.format(which('python')))