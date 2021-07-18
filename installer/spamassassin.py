#!/usr/bin/env python3
#
# MailGuardian installation script
#
import os
import platform
import subprocess
from django.conf import settings
import configparser
import argparse
import distro as distribution
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('-f','--config-file', help='Input path to environment configuration file')

args = parser.parse_args()

def which(program):
    def is_exe(fpath):
        return Path(fpath).is_file() and os.access(fpath, os.X_OK)
    fpath = Path(program)
    if fpath.is_absolute():
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = Path(path, program)
            if is_exe(exe_file):
                return str(exe_file)
    return None

if __name__ == "__main__":
    # First make sure that we are running on Linux
    if platform.system() != 'Linux':
        print('Your operation system is not supported. MailGuardian can only run on Linux')
        exit()
    installer_config = configparser.ConfigParser()
    installer_config.read(args.config_file)
    PKG_MGR = installer_config['bin']['pkg']
    APP_DIR  = installer_config['mailguardian']['app_dir']
    if not installer_config['mailguardian']['api_only']:
        subprocess.call([which('su'), 'postgres -c "createlang plpgsql {}"'.format(installer_config['database']['name'])])
        subprocess.call([which('psql'), '-U {} -f {} {}'.format(installer_config['database']['user'], Path(APP_DIR, 'installer', 'tools', 'bayes.sql')), installer_config['database']['name']])

    conf = []
    conf_index = 0
    with open(Path(installer_config['mailscanner']['config'], 'spamassassin.conf'), 'r') as f:
        conf = f.readlines()

    # TODO: Make version of this that can migrate old data as a django manage.py command
    # Backup current bayes database as root: su -c sa-learn --backup > backup.txt
    # Restore as PSQL after configuration change: su -c sa-learn --restore backup.txt

    # #bayes_auto_expire 0
    for index, line in enumerate(conf):
        if line == '#bayes_auto_expire 0':
            conf_index = index
            break
    
    conf.insert(conf_index + 2, "\n".join([
        'bayes_store_module Mail::SpamAssassin::BayesStore::PgSQL',
        'bayes_sql_dsn      DBI:Pg:{db}:{host}:{port}'.format(db=installer_config['database']['name'], host=installer_config['database']['host'], port=installer_config['database']['port']),
        'bayes_sql_username {}'.format(installer_config['database']['user']),
        'bayes_sql_password {}'.format(installer_config['database']['pass'])
    ]))
