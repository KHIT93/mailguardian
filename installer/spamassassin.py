#!/usr/bin/env python3
#
# MailGuardian installation script
#
import os, sys, platform, subprocess
from django.conf import settings
import configparser
import argparse
import distro as distribution

parser = argparse.ArgumentParser()
parser.add_argument('-f','--config-file', help='Input path to environment configuration file')

args = parser.parse_args()

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
        os.system('su postgres -c "createlang plpgsql {}"'.format(installer_config['database']['name']))
        os.system('psql -U {} -f {} {}'.format(installer_config['database']['user'], os.path.join(APP_DIR, 'installer', 'tools', 'bayes.sql')), installer_config['database']['name'])

    conf = []
    conf_index = 0
    with open(os.path.join(installer_config['mailscanner']['config'], 'spamassassin.conf'), 'r') as f:
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
