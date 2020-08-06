#!/bin/bash
echo 'This script will install MailGuardian, MailScanner and other required components onto the system'
echo ''

LNX_OS_RELEASE=$(grep '^ID=' < /etc/os-release | sed 's/ID="//g' | sed 's/"//g')
if [ -z "$LNX_OS_RELEASE" ]
then
    echo 'Unable to determine Linux version'
    exit 255
fi
export LNX_OS_RELEASE
if [ $LNX_OS_RELEASE == 'centos' ];
then
    LNX_PKG_MGR='yum'
elif [ $LNX_OS_RELEASE == 'Ubuntu' ];
then
    LNX_PKG_MGR='apt'
elif [ $LNX_OS_RELEASE == 'ubuntu' ];
then
    LNX_PKG_MGR='apt'
elif [ $LNX_OS_RELEASE == 'debian' ];
then
    LNX_PKG_MGR='apt'
else
    LNX_OS_RELEASE=$(grep '^ID=' < /etc/os-release | sed 's/ID=//g')
    if [ $LNX_OS_RELEASE == 'centos' ];
    then
        LNX_PKG_MGR='yum'
    elif [ $LNX_OS_RELEASE == 'Ubuntu' ];
    then
        LNX_PKG_MGR='apt'
    elif [ $LNX_OS_RELEASE == 'ubuntu' ];
    then
        LNX_PKG_MGR='apt'
    elif [ $LNX_OS_RELEASE == 'debian' ];
    then
        LNX_PKG_MGR='apt'
    else
        echo 'Unable to determine Linux distribution. Only Debian, Ubuntu and CentOS are supported for this script'
        exit 255
    fi
fi
if ! command -v python3 &> /dev/null
then
    HAS_PY3=0
    if ! command -v python2 &> /dev/null
    then
        echo 'Unable to determine installed python version. We will assume that it is not there'
        HAS_PY3=0
    fi
else
    HAS_PY3=1
fi
export LNX_PKG_MGR
echo ''
echo 'Installing...'
if [[ $HAS_PY3 -eq 0 ]]
then
    echo 'Installing Python 3...'
    if [ $LNX_OS_RELEASE == 'centos' ];
    then
        $LNX_PKG_MGR install -y epel-release
    fi
    $LNX_PKG_MGR install -y python3 python3-setuptools
fi
echo 'Creating application user...'
useradd -m mailguardian
echo 'Installing git commandline tools, if not available...'
$LNX_PKG_MGR install git -y
echo 'Pulling application sourcecode from GitHub...'
su - mailguardian -c 'git clone https://github.com/KHIT93/mailguardian.git /home/mailguardian/mailguardian --branch feature-new-install-scripts'
cd /home/mailguardian/mailguardian || exit
echo 'Installing required packages...'
touch /home/mailguardian/mailguardian/installer.ini
python3 ./installer/deps.py
if ! usermod -a -G mtagroup,postfix mailguardian; then
    echo 'We are really sorry, but something seems to have gone wrong or the script was aborted'
    exit 1
fi
if ! su - mailguardian -c 'cd /home/mailguardian/mailguardian && virtualenv -p python3 . && bin/pip install -r requirements.txt'; then
    echo 'We are really sorry, but something seems to have gone wrong or the script was aborted'
    exit 1
fi
echo 'Installing MailGuardian...'
ENV_DB_PASS=$(date +%s | sha256sum | base64 | head -c 32)
export ENV_DB_PASS
if ! echo 'create database mailguardian;' | su - postgres -c psql; then
    echo 'We are really sorry, but something seems to have gone wrong or the script was aborted'
    exit 1
fi
if ! echo "create user mailguardian with encrypted password '$ENV_DB_PASS';" | su - postgres -c psql; then
    echo 'We are really sorry, but something seems to have gone wrong or the script was aborted'
    exit 1
fi
if ! echo 'grant all privileges on database mailguardian to mailguardian;' | su - postgres -c psql; then
    echo 'We are really sorry, but something seems to have gone wrong or the script was aborted'
    exit 1
fi
if ! bin/python ./installer/mailguardian.py -f /home/mailguardian/mailguardian/installer.ini; then
    echo 'We are really sorry, but something seems to have gone wrong or the script was aborted'
    exit 1
fi
echo 'Configure Postfix...'
if ! bin/python ./installer/postfix.py -f /home/mailguardian/mailguardian/installer.ini; then
    echo 'We are really sorry, but something seems to have gone wrong or the script was aborted'
    exit 1
fi
echo 'Configure MailScanner...'
if ! bin/python ./installer/mailscanner.py -f /home/mailguardian/mailguardian/installer.ini; then
    echo 'We are really sorry, but something seems to have gone wrong or the script was aborted'
    exit 1
fi

spamassassin -D -p /etc/MailScanner/spamassassin.conf --lint
MailScanner --lint

echo 'Installation and initial configuration completed. Now we will perform some cleanup...'
rm -rf /home/mailguardian/mailguardian/installer.ini
echo 'Installation has finished. Please reboot your system and finish the application configuration in your web browser'
exit 0