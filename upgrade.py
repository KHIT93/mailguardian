#!/usr/bin/env python3
#
# MailGuardian upgrade script
#
from django.core.management.utils import get_random_secret_key
from src.core.helpers import which
import os
import json
import platform
import subprocess
from distutils.version import StrictVersion
import importlib.util
import argparse
try:
    from src.mailguardian import settings
except:
    pass

parser = argparse.ArgumentParser()
parser.add_argument('-y','--yes', help='Answer yes to every question and perform update with no interaction', action="store_true")

args = parser.parse_args()

def rebuild_latest_nginx():
    pass

def rebuild_latest_systemd():
    pass

if __name__ == "__main__":
    os.system('clear')
    # First make sure that we are running on Linux
    if platform.system() != 'Linux':
        print('Your operation system is not supported. MailGuardian can only run on Linux')
        exit(255)
    # Get the current directory of this script to determine the path to use
    APP_DIR = os.path.dirname(os.path.abspath(__file__))
    BASE_DIR = os.path.join(APP_DIR,'src')
    DESTINATION_VERSION = '1.0.0'
    if input('This script will evaluate your curren MailGuardian installation and apply any changes necessary. Do you want to start? (y/N) ').lower() != 'y':
        exit(0)
    os.system('clear')
    # Check for legacy configuration file
    if os.path.exists(os.path.join(APP_DIR, 'mailguardian-env.json')):
        config = {}
        for version in os.listdir(os.path.join(APP_DIR,'installer','upgrade')):
            with open(os.path.join(APP_DIR, 'mailguardian-env.json'), 'r') as f:
                config = json.loads(f.read())
            if os.path.isdir(os.path.join(APP_DIR, 'installer', 'upgrade', version)):
                if os.path.isfile(os.path.join(APP_DIR, 'installer', 'upgrade', version, 'upgrade.py')):
                    spec = importlib.util.spec_from_file_location('upgrade.Upgrader', os.path.join(APP_DIR, 'installer', 'upgrade', version, 'upgrade.py'))
                    upgrader = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(upgrader)
                    upgrade = upgrader.Upgrader(config=config, app_dir=APP_DIR, src_dir=BASE_DIR, version=config['config_version'] if 'config_version' in config else '1.0.0')
                    if upgrade.applicable() and upgrade.legacy:
                        if upgrade.upgrade():
                            DESTINATION_VERSION = upgrade.applied_version
    
    # Check if we have new configuration system
    if settings:
        for version in os.listdir(os.path.join(APP_DIR,'installer','upgrade')):
            if os.path.isdir(os.path.join(APP_DIR, 'installer', 'upgrade', version)):
                if os.path.isfile(os.path.join(APP_DIR, 'installer', 'upgrade', version, 'upgrade.py')):
                    spec = importlib.util.spec_from_file_location('upgrade.Upgrader', os.path.join(APP_DIR, 'installer', 'upgrade', version, 'upgrade.py'))
                    upgrader = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(upgrader)
                    upgrade = upgrader.Upgrader(config=settings, app_dir=APP_DIR, src_dir=BASE_DIR, version=settings.LOCAL_CONFIG_VERSION or '1.0.0')
                    if upgrade.applicable():
                        if upgrade.upgrade():
                            DESTINATION_VERSION = upgrade.applied_version
    else:
        print('Could not import application configuration. Aborting')
        exit(255)
    
    print('Now we will perform actions that need to be performed after any file changes')

    # Apply changes that require configuration file changes to have been persisted
    os.system('{0} src/manage.py migrate'.format(which('python')))
    if os.path.exists(os.path.join(APP_DIR, 'mix-manifest.json')) and which('npm'):
        # If we run the frontend, then we will have to perform node updates
        print('Web frontend detected. Rebuilding static assets. This may take some time')
        # os.system('npm install')
        # os.system('npm run production')
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

    print('Your installation has been upgraded to version {version}'.format(version=DESTINATION_VERSION))
    print('If you expected a higher version, please insepct the output from this script to find out what has went wrong')
    
