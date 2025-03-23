#!/usr/bin/env python3
#
# MailGuardian installation script
#
import os, sys, platform, subprocess, argparse, configparser
import distro as distribution

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

CPAN_DEPS = ['CPAN', 'Data::Dumper', 'Data::UUID', 'HTTP::Date', 'DBI', 'Encode::FixLatin', 'Digest::SHA1', 'Mail::SpamAssassin::Plugin::SPF', 'Mail::SpamAssassin::Plugin::URIDNSBL', 'Mail::SpamAssassin::Plugin::DNSEval', 'Encoding::FixLatin']
PKG_MGR = False
installer_config = False

os_postgres_version_map = {
    'debian': {
        '10': '11',
        '11': '13',
    },
    'ubuntu': {
        '20': '12',
        '22': '14'
    },
    'almalinux': {
        '8': '10',
        '9': '13',
    },
    'rocky': {
        '8': '10',
        '9': '13'
    }
}

def get_postgres_distro_version(distro, distro_version):
    if distro in os_postgres_version_map:
        os_disto = os_postgres_version_map[distro]
        if distro_version in os_disto:
            return os_disto[distro_version]
        else:
            return False
    else:
        return False

parser = argparse.ArgumentParser()
parser.add_argument('-f','--config-file', help='Input path to environment configuration file')

args = parser.parse_args()

def setup_deb(pkg_mgr, os_release, os_version):
    print('Setting up on debian-based distro')
    PKG_MGR = which(pkg_mgr)
    os.system('{pkg} update'.format(pkg=PKG_MGR))
    os.system('{pkg} purge postfix -y'.format(pkg=PKG_MGR))
    os.system('{pkg} install sudo wget postfix-pgsql python3 python3-setuptools python3-dev python3-pip libpq-dev nginx ca-certificates openssl libpng-dev lsb-release build-essential postgresql-common -y'.format(pkg=PKG_MGR))
    print('Adding PostgreSQL repository')
    os.system('{sh} /usr/share/postgresql-common/pgdg/apt.postgresql.org.sh'.format(sh=which('sh')))
    os.system('{pkg} update'.format(pkg=PKG_MGR))
    print('Adding Node.js')
    os.system('curl -sL https://deb.nodesource.com/setup_18.x | sudo -E bash -')
    os.system('{pkg} update'.format(pkg=PKG_MGR))
    os.system('{pkg} install nodejs -y'.format(pkg=PKG_MGR))

    if not which('python3'):
        print('python3 was not found on your system. Exitting')
        exit(255)
    postgres_version = get_postgres_distro_version(distro=os_release, distro_version=os_version)
    if not postgres_version:
        print('Your distro {} {} is not known by this script, so we cannot configure the database server.'.format(os_release, os_version))
        exit(255)

    os.system('{pip3} install virtualenv'.format(pip3=which('pip3')))
    pgsql_packages = 'postgresql-server-dev-all postgresql-client'
    if installer_config['database']['db_local']:
        pgsql_packages += ' postgresql'
    os.system('{pkg} install {packages} -y'.format(pkg=PKG_MGR, packages=pgsql_packages))
    os.system('cd /tmp; wget https://github.com/MailScanner/v5/releases/download/5.5.3-2/MailScanner-5.5.3-2.noarch.deb')
    os.system('cd /tmp; dpkg -i MailScanner-5.5.3-2.noarch.deb')
    os.system('/usr/sbin/ms-configure --MTA=none --installClamav=Y --installCPAN=Y --installUnrar=Y --ramdiskSize=0')
    for dep in CPAN_DEPS:
        os.system('{cpan} {dep}'.format(cpan=which('cpan'), dep=dep))
    os.system('{pkg} install libdbd-pg-perl -y'.format(pkg=PKG_MGR))
    if installer_config['database']['db_local']:
        pg_hba_conf = []
        with open(os.path.join('/', 'etc', 'postgresql', postgres_version, 'main', 'pg_hba.conf'), 'r') as f:
            pg_hba_conf = f.readlines()
        for index, line in enumerate(pg_hba_conf):
            if line[:6] == '# IPv4':
                pg_hba_conf.insert(index + 1, 'host    all             all             127.0.0.1/32            md5\n')
            if line[:6] == '# IPv6':
                pg_hba_conf.insert(index + 1, 'host    all             all             ::1/128                 md5\n')
        with open(os.path.join('/', 'etc', 'postgresql', postgres_version, 'main', 'pg_hba.conf'), 'w') as f:
            f.write("".join(pg_hba_conf))
        os.system("{sed} -i \"s/#listen_addresses = 'localhost'/listen_addresses = '*'/g\" {path}".format(sed=which('sed'), path=os.path.join('/', 'etc', 'postgresql', '14', 'main', 'postgresql.conf')))
        os.system('{systemctl} start postgresql@{pg_version}-main'.format(systemctl=which('systemctl'), pg_version=postgres_version))
    os.system('{usermod} -a -G mtagroup nginx'.format(usermod=which('usermod')))

def setup_rhel(pkg_mgr, os_release, os_version):
    print('Setting up on RHEL-based distro')
    PKG_MGR = which(pkg_mgr)
    print('Installing EPEL...')
    os.system('{pkg} install -y epel-release'.format(pkg=PKG_MGR))
    os.system("{sed} -i 's/SELINUX=enforcing/SELINUX=permissive/g' /etc/sysconfig/selinux".format(sed=which('sed')))
    os.system("{sed} -i 's/SELINUX=enforcing/SELINUX=permissive/g' /etc/selinux/config".format(sed=which('sed')))
    if os_version in ['8', '9']:
        postgres_version = get_postgres_distro_version(distro=os_release, distro_version=os_version)
        if not postgres_version:
            print('Your distro {} {} is not known by this script, so we cannot configure the database server.'.format(os_release, os_version))
            exit(255)
        PKG_MGR = which('dnf')
        pgsql_packages = 'postgresql-devel postgresql libpq libpq-devel'
        if installer_config['database']['db_local']:
            pgsql_packages += ' postgresql-server'
        os.system('{pkg} install {packages} -y'.format(pkg=PKG_MGR, packages=pgsql_packages))
        os.system('{pkg} install -y postfix postfix-pgsql'.format(pkg=PKG_MGR))
        os.system('{pkg} groupinstall "Development Tools" -y'.format(pkg=PKG_MGR))
        if os_version == '8':
            os.system('{pkg} install -y python3 python3-devel python3-pip python3-virtualenv python3-setuptools nginx openssl ca-certificates libpng-devel redhat-lsb-core sudo'.format(pkg=PKG_MGR))
        elif os_version == '9':
            os.system('{crb} enable'.format(crb=which('crb')))
            os.system('{pkg} install -y python3 python3-devel python3-pip python3-virtualenv python3-setuptools nginx openssl ca-certificates libpng-devel lsb-release sudo'.format(pkg=PKG_MGR))
        if not which('python3'):
            print('python3 was not found on your system. Exitting')
            exit(255)
    else:
        print('Your version is unfortunately not supported')
        exit(255)
    if installer_config['database']['db_local']:
        os.system(which('postgresql-setup --initdb'))
        pg_hba_conf = []
        with open(os.path.join('/', 'var', 'lib', 'pgsql', postgres_version, 'data', 'pg_hba.conf'), 'r') as f:
            pg_hba_conf = f.readlines()
        for index, line in enumerate(pg_hba_conf):
            if line[:6] == '# IPv4':
                pg_hba_conf.insert(index + 1, 'host    all             all             127.0.0.1/32            md5\n')
            if line[:6] == '# IPv6':
                pg_hba_conf.insert(index + 1, 'host    all             all             ::1/128                 md5\n')
        with open(os.path.join('/', 'var', 'lib', 'pgsql', postgres_version, 'data', 'pg_hba.conf'), 'w') as f:
            f.write("\n".join(pg_hba_conf))
        os.system("{sed} -i \"s/#listen_addresses = 'localhost'/listen_addresses = '*'/g\" {path}".format(sed=which('sed'), path=os.path.join('/', 'var', 'lib', 'pgsql', '14', 'data', 'postgresql.conf')))
        os.system('{systemctl} enable postgresql'.format(systemctl=which('systemctl')))
        os.system('{systemctl} start postgresql'.format(systemctl=which('systemctl')))
        os.system('{cmd} --add-port=5432/tcp --permanent'.format(cmd=which('firewall-cmd')))
    os.system('curl -sL https://rpm.nodesource.com/setup_18.x | sudo bash -')
    os.system('{pkg} install -y nodejs'.format(pkg=PKG_MGR))
    os.system('{pkg} install https://github.com/MailScanner/v5/releases/download/5.5.3-2/MailScanner-5.5.3-2.rhel.noarch.rpm -y'.format(pkg=PKG_MGR))
    os.system('/usr/sbin/ms-configure --MTA=none --installEPEL=Y --installClamav=Y --configClamav=Y --installTNEF=Y --installUnrar=Y --installidn=Y --SELPermissive=Y --installCPAN=Y --ignoreDeps=Y --ramdiskSize=0')
    for dep in CPAN_DEPS:
        os.system('{cpan} {dep}'.format(cpan=which('cpan'), dep=dep))
    os.system('{pkg} install perl-DBD-Pg -y'.format(pkg=PKG_MGR))
    os.system('{systemctl} enable mailscanner'.format(systemctl=which('systemctl')))
    os.system('{systemctl} enable msmilter'.format(systemctl=which('systemctl')))
    os.system('{cmd} --add-service=smtp --permanent'.format(cmd=which('firewall-cmd')))
    os.system('{cmd} --add-service=smtps --permanent'.format(cmd=which('firewall-cmd')))
    os.system('{cmd} --add-service=http --permanent'.format(cmd=which('firewall-cmd')))
    os.system('{cmd} --add-service=https --permanent'.format(cmd=which('firewall-cmd')))
    os.system('{cmd} --reload'.format(cmd=which('firewall-cmd')))
    os.system('{usermod} -a -G mail nginx'.format(usermod=which('usermod')))

if __name__ == "__main__":
    # First make sure that we are running on Linux
    if platform.system() != 'Linux':
        print('Your operation system is not supported. MailGuardian can only run on Linux')
        exit()
    # Detect the Linux distribution
    # If we can detect you specific Linux distribution,
    # we will skip the parts where we configure systemd,
    # and your webserver
    installer_config = configparser.RawConfigParser()
    installer_config.read(args.config_file)
    distro = distribution.id()
    distro_version = distribution.version().split('.')[0]
    if distro in ['rocky', 'almalinux']:
        PKG_MGR = 'dnf'
        setup_rhel(PKG_MGR, distro, distro_version)
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
