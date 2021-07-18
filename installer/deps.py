#!/usr/bin/env python3
#
# MailGuardian installation script
#
import os
import platform
import subprocess
import argparse
import configparser
import distro as distribution
from pathlib import Path

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

CPAN_DEPS = ['CPAN', 'Data::Dumper', 'Data::UUID', 'HTTP::Date', 'DBI', 'Encode::FixLatin', 'Digest::SHA1', 'Mail::ClamAV', 'Mail::SpamAssassin::Plugin::SPF', 'Mail::SpamAssassin::Plugin::URIDNSBL', 'Mail::SpamAssassin::Plugin::DNSEval']
PKG_MGR = False
installer_config = False

parser = argparse.ArgumentParser()
parser.add_argument('-f','--config-file', help='Input path to environment configuration file')

args = parser.parse_args()

def setup_deb(pkg_mgr, os_release, os_version):
    print('Setting up on debian-based distro')
    PKG_MGR = which(pkg_mgr)
    subprocess.call([PKG_MGR, 'update'])
    subprocess.call([PKG_MGR, 'purge postfix -y'])
    subprocess.call([PKG_MGR, 'install sudo wget postfix-pgsql python3 python3-setuptools python3-dev python3-pip libpq-dev nginx ca-certificates openssl libpng-dev lsb-release build-essential postgresql-common -y'])
    if os_release == 'debian':
        print('Adding additional repositories')
        subprocess.call(['echo "deb http://deb.debian.org/debian $(lsb_release -cs)-backports main" > /etc/apt/sources.list.d/debian-backports.list'])
        subprocess.call([PKG_MGR, 'update'])
    print('Adding PostgreSQL repository')
    subprocess.call([which('sh'), '/usr/share/postgresql-common/pgdg/apt.postgresql.org.sh'])
    subprocess.call([PKG_MGR, 'update'])
    print('Adding Node.js')
    subprocess.call([which('curl') + ' -sL https://deb.nodesource.com/setup_14.x | sudo -E bash -'])
    subprocess.call([PKG_MGR, 'update'])
    subprocess.call([PKG_MGR, 'install nodejs -y'])

    if not which('python3'):
        print('python3 was not found on your system. Exitting')
        exit(255)
    subprocess.call([which('pip3'), 'install virtualenv'])
    pgsql_packages = 'postgresql-server-dev-12 postgresql-client-12'
    if installer_config['database']['db_local']:
        pgsql_packages += ' postgresql-12'
    subprocess.call([PKG_MGR, 'install {packages}'.format(packages=pgsql_packages)])
    subprocess.call([which('cd') + ' /tmp; wget https://github.com/MailScanner/v5/releases/download/5.3.4-3/MailScanner-5.3.4-3.noarch.deb'])
    subprocess.call([which('cd') + ' /tmp; dpkg -i MailScanner-5.3.4-3.noarch.deb'])
    subprocess.call(['/usr/sbin/ms-configure --MTA=none --installClamav=Y --installCPAN=Y --ignoreDeps=Y --ramdiskSize=0'])
    for dep in CPAN_DEPS:
        subprocess.call(['{cpan} -i {dep}'.format(cpan=which('cpan'), dep=dep)])
    subprocess.call([PKG_MGR, 'install libdbd-pg-perl -y'])
    if installer_config['database']['db_local']:
        pg_hba_conf = []
        with open(Path('/', 'etc', 'postgresql', '12', 'main', 'pg_hba.conf'), 'r') as f:
            pg_hba_conf = f.readlines()
        for index, line in enumerate(pg_hba_conf):
            if line[:6] == '# IPv4':
                pg_hba_conf.insert(index + 1, 'host    all             all             127.0.0.1/32            md5\n')
            if line[:6] == '# IPv6':
                pg_hba_conf.insert(index + 1, 'host    all             all             ::1/128                 md5\n')
        with open(Path('/', 'etc', 'postgresql', '12', 'main', 'pg_hba.conf'), 'w') as f:
            f.write("".join(pg_hba_conf))
        subprocess.call([which('sed'), "-i 's/#listen_address = \'localhost\'/listen_address = \'*\'/g", Path('/', 'etc', 'postgresql', '12', 'main', 'postgresql.conf')])
        subprocess.call([which('systemctl'), 'start postgresql@12-main.service'])
    subprocess.call([which('usermod'), '-a -G mtagroup nginx'])

def setup_rhel(pkg_mgr, os_release, os_version):
    print('Setting up on RHEL-based distro')
    PKG_MGR = which(pkg_mgr)
    print('Installing EPEL...')
    subprocess.call([PKG_MGR, 'install -y epel-release'])
    if os_release == 'centos':
        subprocess.call([PKG_MGR, 'install -y centos-release-scl'])
    subprocess.call([which('sed'), "-i 's/SELINUX=enforcing/SELINUX=permissive/g' /etc/sysconfig/selinux"])
    if os_version == '7':
        print('Adding GhettoForge repo...')
        # GhettoForge currently give postfix 3.5.3
        subprocess.call([PKG_MGR, '--nogpg install https://mirror.ghettoforge.org/distributions/gf/gf-release-latest.gf.el7.noarch.rpm -y'])
        subprocess.call([PKG_MGR, 'clean all'])
        subprocess.call([PKG_MGR, 'makecache fast'])
        subprocess.call([PKG_MGR, 'remove postfix -y'])
        subprocess.call([PKG_MGR, 'install https://download.postgresql.org/pub/repos/yum/reporpms/EL-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm -y'])
        pgsql_packages = 'postgresql12-devel postgresql12 libpq5 libpq5-devel'
        if installer_config['database']['db_local']:
            pgsql_packages += ' postgresql12-server'
        subprocess.call([PKG_MGR, 'install {packages} -y'.format(packages=pgsql_packages)])
        subprocess.call([PKG_MGR, 'install --enablerepo=gf-plus postfix3 postfix3-pgsql -y'])

    elif os_version == '8':
        PKG_MGR = which('dnf')
        subprocess.call([PKG_MGR, 'install https://download.postgresql.org/pub/repos/yum/reporpms/EL-8-x86_64/pgdg-redhat-repo-latest.noarch.rpm -y'])
        subprocess.call([PKG_MGR, '-qy module disable postgresql'])
        pgsql_packages = 'postgresql12-devel postgresql12 libpq5 libpq5-devel'
        if installer_config['database']['db_local']:
            pgsql_packages += ' postgresql12-server'
        subprocess.call([PKG_MGR, 'install {packages}'.format(packages=pgsql_packages)])
        subprocess.call([PKG_MGR, 'install -y postfix postfix-pgsql'])
    else:
        print('Your version is unfortunately not supported')
        exit(255)
    
    subprocess.call([PKG_MGR, 'groupinstall "Development Tools" -y'])
    subprocess.call([PKG_MGR, 'install -y python3 python3-devel python3-pip python3-setuptools nginx openssl ca-certificates libpng-devel redhat-lsb-core sudo'])
    if not which('python3'):
        print('python3 was not found on your system. Exitting')
        exit(255)
    subprocess.call([which('pip3'), 'install virtualenv'])
    if installer_config['database']['db_local']:
        subprocess.call(['/usr/pgsql-12/bin/postgresql-12-setup initdb'])
        pg_hba_conf = []
        with open(Path('/', 'var', 'lib', 'pgsql', '12', 'data', 'pg_hba.conf'), 'r') as f:
            pg_hba_conf = f.readlines()
        for index, line in enumerate(pg_hba_conf):
            if line[:6] == '# IPv4':
                pg_hba_conf.insert(index + 1, 'host    all             all             127.0.0.1/32            md5\n')
            if line[:6] == '# IPv6':
                pg_hba_conf.insert(index + 1, 'host    all             all             ::1/128                 md5\n')
        with open(Path('/', 'var', 'lib', 'pgsql', '12', 'data', 'pg_hba.conf'), 'w') as f:
            f.write("\n".join(pg_hba_conf))
        subprocess.call([which('sed'), "-i 's/#listen_address = \'localhost\'/listen_address = \'*\'/g'", Path('/', 'var', 'lib', 'pgsql', '12', 'data', 'postgresql.conf')])
        subprocess.call([which('systemctl', 'enable --now postgresql-12')])
        subprocess.call([which('firewall-cmd'), '--add-port=5432/tcp --permanent'])
    subprocess.call([which('curl'), '-sL https://rpm.nodesource.com/setup_14.x | sudo bash -'])
    subprocess.call([PKG_MGR, 'install nodejs -y'])
    subprocess.call([PKG_MGR, 'install https://github.com/MailScanner/v5/releases/download/5.3.4-3/MailScanner-5.3.4-3.rhel.noarch.rpm -y'])
    subprocess.call(['/usr/sbin/ms-configure --installEPEL=Y --MTA=none --installClamav=Y --installCPAN=Y --ramdiskSize=0 --SELPermissive=Y --installDf=Y --installUnrar=Y --installTNEF=Y --configClamav=Y --installPowerTools=Y'])
    for dep in CPAN_DEPS:
        subprocess.call(['{cpan} -i {dep}'.format(cpan=which('cpan'), dep=dep)])
    subprocess.call([PKG_MGR, 'install perl-DBD-Pg -y'])
    subprocess.call([which('systemctl'), 'enable --now mailscanner'])
    subprocess.call([which('systemctl'), 'enable --now msmilter'])
    subprocess.call([which('firewall-cmd'), '--add-service=smtp --permanent'])
    subprocess.call([which('firewall-cmd'), '--add-service=smtps --permanent'])
    subprocess.call([which('firewall-cmd'), '--add-service=http --permanent'])
    subprocess.call([which('firewall-cmd'), '--add-service=https --permanent'])
    subprocess.call([which('firewall-cmd', '--reload')])
    subprocess.call([which('usermod'), '-a -G mail nginx'])

if __name__ == "__main__":
    # First make sure that we are running on Linux
    if platform.system() != 'Linux':
        print('Your operation system is not supported. MailGuardian can only run on Linux')
        exit()
    # Detect the Linux distribution
    # If we can detect you specific Linux distribution,
    # we will skip the parts where we configure systemd,
    # and your webserver
    installer_config = configparser.ConfigParser()
    installer_config.read(args.config_file)
    distro_data = distribution.linux_distribution(full_distribution_name=False)
    distro = distro_data[0] or 'LINUX'
    distro_version = distro_data[1] or '0'
    distro_version_codename = distro_data[2] or 'Core'
    if distro in ['centos', 'rocky', 'almalinux', 'rhel']:
        PKG_MGR = 'dnf' if distro_version[0] == '8' else 'yum'
        setup_rhel(PKG_MGR, distro, distro_version[0])
        exit(0)
    elif distro == 'debian':
        PKG_MGR = 'apt'
        setup_deb(PKG_MGR, distro, distro_version)
        exit(0)
    elif distro.lower() == 'ubuntu':
        PKG_MGR = 'apt'
        setup_deb(PKG_MGR, distro, distro_version)
        exit(0)
    else:
        print('Your Linux distribution or version is not supported')
        print(distro)
        exit(255)
