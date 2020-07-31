#!/usr/bin/env python3
#
# MailGuardian installation script
#
import os, sys, platform

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

def setup_deb():
    print('Setting up on debian-based distro')
    os.system('{apt} update'.format(apt=PKG_MGR))
    os.system('{apt} install sudo wget postfix-pgsql python3 python3-setuptools python3-dev libpq-dev nginx ca-certificates openssl libpng-dev lsb-release -y'.format(apt=PKG_MGR))
    if platform.linux_distribution()[0] == 'debian':
        print('Adding additional repositories')
        os.system('echo "deb http://deb.debian.org/debian $(lsb_release -cs)-backports main" > /etc/apt/sources.list.d/debian-backports.list')
        os.system('{apt} update'.format(apt=PKG_MGR))
    print('Adding PostgreSQL repository')
    os.system('echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list')
    os.system('wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -')
    os.system('{apt} update'.format(apt=PKG_MGR))
    if not which('python3'):
        print('python3 was not found on your system. Exitting')
        exit(255)
    os.system('{python} /usr/lib/python3/dist-packages/easy_install.py virtualenv pip'.format(python=which('python3')))
    pgsql_packages = 'postgresql-server-dev-12 postgresql-client-12'
    if input('Does this system run the PostgreSQL database server? (y/N) ').lower() == 'y':
        pgsql_packages += 'postgresql-12'
    os.system('{apt} {packages} -y'.format(apt=PKG_MGR, packages=pgsql_packages))
    os.system('cd /tmp; wget https://github.com/MailScanner/v5/releases/download/5.3.3-1/MailScanner-5.3.3-1.noarch.deb')
    os.system('cd /tmp; dpkg -i MailScanner-5.3.3-1.noarch.deb')
    os.system('/usr/sbin/ms-configure --MTA=postfix --installClamav=Y --installCPAN=Y --ignoreDeps=Y --ramdiskSize=0')
    for dep in CPAN_DEPS:
        os.system('cpan -i {dep}'.format(dep=dep))

def setup_rhel():
    print('Setting up on RHEL-based distro')

if __name__ == "__main__":
    # First make sure that we are running on Linux
    if platform.system() != 'Linux':
        print('Your operation system is not supported. MailGuardian can only run on Linux')
        exit()
    PKG_MGR = None
    CPAN_DEPS = ['CPAN', 'Data::Dumper', 'Data::UUID', 'HTTP::Date', 'DBI', 'DBD::Pg', 'Encode::FixLatin', 'Digest::SHA1', 'Mail::ClamAV', 'Mail::SpamAssassin::Plugin::SPF', 'Mail::SpamAssassin::Plugin::URIDNSBL', 'Mail::SpamAssassin::Plugin::DNSEval']
    # Detect the Linux distribution
    # If we can detect you specific Linux distribution,
    # we will skip the parts where we configure systemd,
    # and your webserver
    distro = platform.linux_distribution()
    if distro[0] == 'CentOS Linux':
        PKG_MGR = which('yum')
        setup_rhel()
        exit(0)
    elif distro[0] == 'debian':
        PKG_MGR = which('apt')
        if int(distro[1].replace('.', '')) <= 90:
            print('Your version of Debian is not supported')
            exit(255)
        setup_deb()
        exit(0)
    elif distro[0] == 'Ubuntu':
        PKG_MGR = which('apt')
        if int(distro[1].replace('.', '')) <= 1604:
            print('Your version of Ubuntu is not supported')
            exit(255)
        setup_deb()
        exit(0)
    else:
        print('Your Linux distribution or version is not supported')
        print(distro)
        exit(255)
