#!/usr/bin/env python3
#
# MailGuardian installation script
#
import os, sys, platform
from django.conf import settings

def which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None

if __name__ == "__main__":
    # First make sure that we are running on Linux
    if platform.system() != 'Linux':
        print('Your operation system is not supported. MailGuardian can only run on Linux')
        exit()
    PKG_MGR = None
    POSTFIX_DIR = '/etc/postfix'
    APP_DIR  = os.environ['MAILGUARDIAN_APP_DIR']
    # Detect the Linux distribution
    # If we can detect you specific Linux distribution,
    # we will skip the parts where we configure systemd,
    # and your webserver
    distro = platform.linux_distribution()
    if distro[0] == 'CentOS Linux':
        PKG_MGR = which('yum')
    elif distro[0] == 'debian':
        PKG_MGR = which('apt')
        if int(distro[1].replace('.', '')) <= 90:
            print('Your version of Debian is not supported')
            exit(255)
    elif distro[0] == 'Ubuntu':
        PKG_MGR = which('apt')
        if int(distro[1].replace('.', '')) <= 1604:
            print('Your version of Ubuntu is not supported')
            exit(255)
    else:
        print('Your Linux distribution or version is not supported')
        print(distro)
        exit(255)
    main_cf = []
    with open(os.path.join(POSTFIX_DIR, 'main.cf'), 'r') as f:
        main_cf = f.readlines()
    for index, line in enumerate(main_cf):
        if line[:12] == 'mynetworks =':
            main_cf[index] += ', proxy:pgsql:{postfix}/pgsql-mynetworks.cf'.format(postfix=POSTFIX_DIR)
    main_cf.append('header_checks = regexp:/{postfix}/header_checks'.format(postfix=POSTFIX_DIR))
    main_cf.append('relay_domains = regexp:/{postfix}/pgsql-transport.cf'.format(postfix=POSTFIX_DIR))
    main_cf.append('transport_maps = regexp:/{postfix}/pgsql-transport.cf'.format(postfix=POSTFIX_DIR))
    with open(os.path.join(POSTFIX_DIR, 'main.cf'), 'w') as f:
        f.writelines(main_cf)
    os.system('echo "/^Received:\ from\ {hostname}\ \(localhost\ \[127.0.0.1/ IGNORE" > {postfix}/header_checks'.format(postfix=POSTFIX_DIR, hostname=os.environ['MAILGUARDIAN_APP_HOSTNAME']))
    os.system('echo "/^Received:\ from\ {hostname}\ \(localhost\ \[::1/ IGNORE" >> {postfix}/header_checks'.format(postfix=POSTFIX_DIR, hostname=os.environ['MAILGUARDIAN_APP_HOSTNAME']))
    os.system('echo "/^Received:\ from\ localhost\ \(localhost\ \[127.0.0.1/ IGNORE" >> {postfix}/header_checks'.format(postfix=POSTFIX_DIR))

    print('Configure PostgreSQL integrations')
    with open(os.path.join(POSTFIX_DIR, 'pgsql-transport.cf')) as f:
        f.writelines([
            "user = {}".format(os.environ['MAILGUARDIAN_DB_USER']),
            "password = {}".format(os.environ['MAILGUARDIAN_DB_PASS']),
            "hosts = {}".format(os.environ['MAILGUARDIAN_DB_HOST'] + ':' + os.environ['MAILGUARDIAN_DB_PORT'] if os.environ['MAILGUARDIAN_DB_PORT'] != '5432' else os.environ['MAILGUARDIAN_DB_HOST']),
            "dbname = {}".format(os.environ['MAILGUARDIAN_DB_NAME']),
            "query = SELECT CONCAT(relay_type,':[',destination,']') from domains_domain where name='\%\s' AND active = '1';",
        ])

    with open(os.path.join(POSTFIX_DIR, 'pgsql-mynetworks.cf')) as f:
        f.writelines([
            "user = {}".format(os.environ['MAILGUARDIAN_DB_USER']),
            "password = {}".format(os.environ['MAILGUARDIAN_DB_PASS']),
            "hosts = {}".format(os.environ['MAILGUARDIAN_DB_HOST'] + ':' + os.environ['MAILGUARDIAN_DB_PORT'] if os.environ['MAILGUARDIAN_DB_PORT'] != '5432' else os.environ['MAILGUARDIAN_DB_HOST']),
            "dbname = {}".format(os.environ['MAILGUARDIAN_DB_NAME']),
            "query = query = SELECT ip_address from mail_smtprelay where (ip_address='\%\s' or hostname='\%\s') AND active = '1';",
        ])
