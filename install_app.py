#!/usr/bin/env python3

# START: Copy of https://github.com/tartley/colorama/blob/master/colorama/ansi.py

CSI = '\033['
OSC = '\033]'
BEL = '\a'


def code_to_chars(code):
    return CSI + str(code) + 'm'

class AnsiCodes(object):
    def __init__(self):
        # the subclasses declare class attributes which are numbers.
        # Upon instantiation we define instance attributes, which are the same
        # as the class attributes but wrapped with the ANSI escape sequence
        for name in dir(self):
            if not name.startswith('_'):
                value = getattr(self, name)
                setattr(self, name, code_to_chars(value))

class AnsiFore(AnsiCodes):
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37
    RESET = 39

class AnsiBack(AnsiCodes):
    BLACK = 40
    RED = 41
    GREEN = 42
    YELLOW = 43
    BLUE = 44
    MAGENTA = 45
    CYAN = 46
    WHITE = 47
    RESET = 49

class AnsiStyle(AnsiCodes):
    BRIGHT = 1
    DIM = 2
    NORMAL = 22
    RESET_ALL = 0

Fore = AnsiFore()
Back = AnsiBack()
Style = AnsiStyle()

# END: Copy of https://github.com/tartley/colorama/blob/master/colorama/ansi.py

RHEL_DISTROS = [
    'centos',
    'almalinux',
    'rocky',
    'rhel'
]
DEBIAN_DISTROS = [
    'debian',
    'ubuntu'
]

SUPPORTED_LINUX_DISTROS = RHEL_DISTROS + DEBIAN_DISTROS

PKG_MGRS = {
    'debian': 'apt',
    'ubuntu': 'apt',
    'centos': 'yum',
    'almalinux': 'dnf',
    'rocky': 'dnf',
    'rhel': 'dnf'
}

def print_info(message):
    print(Fore.CYAN + message + Style.RESET_ALL)

def print_warning(message):
    print(Fore.YELLOW + message + Style.RESET_ALL)

def print_error(message):
    print(Fore.RED + message + Style.RESET_ALL)

def print_success(message):
    print(Fore.GREEN + message + Style.RESET_ALL)

from pathlib import Path
import subprocess
import argparse
import platform
import time
import os
from distutils.version import LooseVersion

if not platform.system() == 'Linux':
    print('*** Installation is only supported on Linux ***')
    exit(255)

try:
    import requests
except:
    print_error('*** Could not import requests library ***')
    print_info('*** Often it can be fixed by installing python3-requests ***')
    exit(255)

get_os_data = False

try:
    get_os_data = platform.freedesktop_os_release
except AttributeError:
    print_warning('*** Patching Python %s with platform.freedesktop_os_release from Python 3.10.x ***' % (platform.python_version(),))
    import re
    ### freedesktop.org os-release standard
    # https://www.freedesktop.org/software/systemd/man/os-release.html

    # NAME=value with optional quotes (' or "). The regular expression is less
    # strict than shell lexer, but that's ok.
    _os_release_line = re.compile(
        "^(?P<name>[a-zA-Z0-9_]+)=(?P<quote>[\"\']?)(?P<value>.*)(?P=quote)$"
    )
    # unescape five special characters mentioned in the standard
    _os_release_unescape = re.compile(r"\\([\\\$\"\'`])")
    # /etc takes precedence over /usr/lib
    _os_release_candidates = ("/etc/os-release", "/usr/lib/os-release")
    _os_release_cache = None
    def _parse_os_release(lines):
        # These fields are mandatory fields with well-known defaults
        # in practice all Linux distributions override NAME, ID, and PRETTY_NAME.
        info = {
            "NAME": "Linux",
            "ID": "linux",
            "PRETTY_NAME": "Linux",
        }

        for line in lines:
            mo = _os_release_line.match(line)
            if mo is not None:
                info[mo.group('name')] = _os_release_unescape.sub(
                    r"\1", mo.group('value')
                )

        return info
    def freedesktop_os_release():
        """Return operation system identification from freedesktop.org os-release
        """
        global _os_release_cache

        if _os_release_cache is None:
            errno = None
            for candidate in _os_release_candidates:
                try:
                    with open(candidate, encoding="utf-8") as f:
                        _os_release_cache = _parse_os_release(f)
                    break
                except OSError as e:
                    errno = e.errno
            else:
                raise OSError(
                    errno,
                    f"Unable to read files {', '.join(_os_release_candidates)}"
                )

        return _os_release_cache.copy()
    
    get_os_data = freedesktop_os_release
    
if not get_os_data:
    print_error('*** Unable to initialize OS detection logic ***')
    exit(255)

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

parser = argparse.ArgumentParser()
parser.add_argument('--version', help='Display the script version', action='store_true')
parser.add_argument('-r', '--release', help='Specific release version of MailGuardian to install')
parser.add_argument('-b', '--branch', help='Install from latest commit to this branch')

args = parser.parse_args()

if __name__ == "__main__":    
    os_data = get_os_data()
    platform_os_id = str(os_data.get('ID', False)).lower()
    if not platform_os_id in SUPPORTED_LINUX_DISTROS:
        print_error('*** Linux Distribution %s is not supported ***' % (platform_os_id,))
        print_warning('These Linux distributions are supported:\n%s' % (", ".join(SUPPORTED_LINUX_DISTROS),))
        exit(255)

    # Check if we are root or using sudo
    if os.geteuid() != 0:
        print_error('*** In order to install MailGuardian, this script must be executed with either sudo or as root! ***')
        exit(255)

    releases = []
    to_install = False
    if args.branch:
        response = requests.get('https://api.github.com/repos/khit93/mailguardian/branches')
        if not response.status_code == 200:
            print_error('*** Could not verify available branches. Got HTTP error code %s ***' % (response.status_code,))
        branches = [branch['name'] for branch in response.json()]
        if not args.branch in branches:
            print_error('*** %s is not a supported release tag for MailGuardian ***' % (args.branch,))
            print_error('*** The following branches are valid: ***')
            print(", ".join(branches))
            exit(255)
        else:
            to_install = args.branch
    else:
        response = requests.get('https://api.github.com/repos/khit93/mailguardian/releases')
        if not response.status_code == 200:
            print_error('*** Could not verify available releases. Got HTTP error code %s ***' % (response.status_code,))
        for release in response.json():
            releases.append(release['name'])
        releases.sort(key=LooseVersion, reverse=True)
        if not args.release:
            to_install = releases[0]
        elif args.release in releases:
            to_install = args.release
        else:
            print_error('*** %s is not a supported release tag for MailGuardian ***' % (args.release,))
            print_error('*** The following release tags are valid: ***')
            print(", ".join(releases))
            exit(255)

    if not to_install:
        print_warning('*** No release tag or branch selected ***')
        print_error('*** No installation source defined. Aborting... ***')
        exit(255)

    # Start the installation
    if platform_os_id in RHEL_DISTROS:
        print_warning('*** Installation of RHEL requires EPEL. Installing it now ***')
        subprocess.check_call('%s install -y %s' % (PKG_MGRS[platform_os_id], 'epel-release'), shell=True)
    print_info('*** Installing setuptools ***')
    if platform_os_id in RHEL_DISTROS:
        subprocess.check_call('%s install -y %s' % (PKG_MGRS[platform_os_id], 'python38-setuptools'), shell=True)
    else:
        subprocess.check_call('%s install -y %s' % (PKG_MGRS[platform_os_id], 'python3-setuptools'), shell=True)
    print_info('*** Installing PIP ***')
    if platform_os_id in RHEL_DISTROS:
        subprocess.check_call('%s install -y %s' % (PKG_MGRS[platform_os_id], 'python38-pip'), shell=True)
    else:
        subprocess.check_call('%s install -y %s' % (PKG_MGRS[platform_os_id], 'python3-pip'), shell=True)
    print_info('*** Installing VIRTUALENV ***')
    if platform_os_id in RHEL_DISTROS:
        subprocess.check_call('%s install %s' % ('pip3', 'virtualenv'), shell=True)
    else:
        subprocess.check_call('%s install -y %s' % (PKG_MGRS[platform_os_id], 'python3-virtualenv'), shell=True)
    if LooseVersion(to_install) < LooseVersion('3.0.0'):
        # Installing for v2 or below, so we need pytz
        print_info('*** Installing PYTZ ***')
        if platform_os_id in RHEL_DISTROS:
            subprocess.check_call('%s install -y %s' % (PKG_MGRS[platform_os_id], 'python38-pytz'), shell=True)
        else:
            subprocess.check_call('%s install -y %s' % (PKG_MGRS[platform_os_id], 'python3-pytz'), shell=True)
    print_info('*** Installing required python libraries ***')
    subprocess.check_call('pip3 install distro', shell=True)
    print_info('*** Installing GIT ***')
    subprocess.check_call('%s install -y %s' % (PKG_MGRS[platform_os_id], 'git'), shell=True)

    print_info('*** Creating MailGuardian application user ***')
    subprocess.check_call('useradd -m mailguardian', shell=True)
    subprocess.check_call('chmod 755 /home/mailguardian', shell=True)
    print_info('*** Downloading MailGuardian %s ***' % (to_install,))
    subprocess.check_call("su - mailguardian -c 'git clone https://github.com/KHIT93/mailguardian.git --branch %s /home/mailguardian/mailguardian'" % (to_install,), shell=True)
    # TODO: Move this into installer/configure.py
    database_password_suggestion = subprocess.check_output('echo $(date +%s | sha256sum | base64 | head -c 32)', shell=True).decode().strip()
    
    print_info('*** Starting application configuration wizard ***')
    try:
        subprocess.check_call('ENV_DB_PASS="%s" python3 /home/mailguardian/mailguardian/installer/configure.py -f /home/mailguardian/mailguardian/installer.ini' % (database_password_suggestion,), shell=True)
    except:
        print_error('We are really sorry, but something has gone wrong during initial steps of installation. Please fix the errors above and try again')
        exit(255)
    
    if not Path('/home/mailguardian/mailguardian/installer.ini').exists():
        print_error('We are really sorry, but it appears as if we are unable to create the configuration file for the installation script. Please check the error above and try again')
        exit(255)
    
    print_info('*** Installing required dependencies ***')
    try:
        subprocess.check_call('python3 /home/mailguardian/mailguardian/installer/deps.py -f /home/mailguardian/mailguardian/installer.ini', shell=True)
    except:
        print_error('We are really sorry, but something has gone wrong during initial steps of installation. Please fix the errors above and try again')
        exit(255)
    
    print_info('*** Assigning permission for MailGuardian ***')
    try:
        subprocess.check_call('usermod -a -G mtagroup,postfix mailguardian', shell=True)
    except:
        print_error('We are really sorry, but something seems to have gone wrong or the script was aborted')
        exit(255)
    
    print_info('*** Installing application libraries ***')
    try:
        subprocess.check_call("su - mailguardian -c 'cd /home/mailguardian/mailguardian && virtualenv -p python3 . && bin/pip install -r requirements.txt'", shell=True)
    except:
        print_error('We are really sorry, but something seems to have gone wrong or the script was aborted')
        exit(255)
    
    print_info('*** Installing MailGuardian ***')
    print_info('This could take quite a bit of time to complete')

    print_info('*** Creating database ***')
    try:
        subprocess.check_call("echo 'create database mailguardian;' | su - postgres -c psql", shell=True)
    except:
        print_error('We are really sorry, but it seems that something went wrong during creation of the database')
        exit(255)
    
    try:
        subprocess.check_call('echo "create user mailguardian with encrypted password \'$ENV_DB_PASS\';" | su - postgres -c psql', shell=True)
    except:
        print_error('We are really sorry, but it seems that something went wrong during creation of the database')
        exit(255)
    
    try:
        subprocess.check_call("echo 'grant all privileges on database mailguardian to mailguardian;' | su - postgres -c psql", shell=True)
    except:
        print_error('We are really sorry, but it seems that something went wrong during creation of the database')
        exit(255)
    
    print_info('*** Configuring MailGuardian ***')
    try:
        subprocess.check_call('/home/mailguardian/mailguardian/bin/python /home/mailguardian/mailguardian/installer/mailguardian.py -f /home/mailguardian/mailguardian/installer.ini', shell=True)
    except:
        print_error('We are really sorry, but something seems to have gone wrong or the script was aborted')
        exit(255)

    print_info('*** Configuring Postfix ***')
    try:
        subprocess.check_call('/home/mailguardian/mailguardian/bin/python /home/mailguardian/mailguardian/installer/postfix.py -f /home/mailguardian/mailguardian/installer.ini', shell=True)
    except:
        print_error('We are really sorry, but something seems to have gone wrong or the script was aborted')
        exit(255)

    print_info('*** Configuring SpamAssassin ***')
    try:
        subprocess.check_call('/home/mailguardian/mailguardian/bin/python /home/mailguardian/mailguardian/installer/spamassassin.py -f /home/mailguardian/mailguardian/installer.ini', shell=True)
    except:
        print_error('We are really sorry, but something seems to have gone wrong or the script was aborted')
        exit(255)

    print_info('*** Configuring MailScanner ***')
    try:
        subprocess.check_call('/home/mailguardian/mailguardian/bin/python /home/mailguardian/mailguardian/installer/mailscanner.py -f /home/mailguardian/mailguardian/installer.ini', shell=True)
    except:
        print_error('We are really sorry, but something seems to have gone wrong or the script was aborted')
        exit(255)

    print_info('*** Installing application frontend UI ***')
    try:
        subprocess.check_call("su - mailguardian -c 'cd /home/mailguardian/mailguardian; npm install; npm run production'", shell=True)
    except:
        print_error('We are really sorry, but something seems to have gone wrong or the script was aborted')
        exit(255)

    print_info('*** Starting virus scanners ***')
    time.sleep(20)

    print_info('*** Testing configuration of spamassassin ***')
    subprocess.call('spamassassin -D -p /etc/MailScanner/spamassassin.conf --lint', shell=True)

    print_info('*** Testing MailScanner configuration ***')
    subprocess.call('MailScanner --lint', shell=True)

    