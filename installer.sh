#!/bin/bash
echo 'This script will install MailGuardian, MailScanner and other required components onto the system'
echo ''
if ! command -v python3 &> /dev/null
then
    HAS_PY3 = 0
    if ! command -v python2 &> /dev/null
    then
        echo 'Unable to determine installed python version'
        exit 255
    else
        LNX_OS_RELEASE=$(python2 -c 'import platform; print platform.linux_distribution()[0]')
    fi
else
    HAS_PY3=1
    # Python 3.8 no longer contains platform.dist() and platform.linux_distribution()
    # A workaround has to be provided here
    read -r -d '' PY_OS_FIND <<- EOM
    with open('/etc/os-release', 'r') as f:\n\t
    for l in f.readlines():\n\t\t
        if l[:3] == 'ID=':\n\t\t\t
            print(l.replace('ID=','').strip())\n\t\t\t
            break
EOM
    LNX_OS_RELEASE=$(echo -e $PY_OS_FIND | python3)
    if [ -z $LNX_OS_RELEASE ]
    then
        echo 'Unable to determine Linux version'
        exit 255
    fi
fi
if [[ $LNX_OS_RELEASE -eq 'ubuntu' ]]
then
    LNX_PKG_MGR='apt'
elif [[ $LNX_OS_RELEASE -eq 'debian' ]]
then
    LNX_PKG_MGR='apt'
elif [[ $LNX_OS_RELEASE -eq 'centos' ]]
then
    LNX_PKG_MGR='yum'
else
    echo 'Unable to determine Linux distribution. Only Debian, Ubuntu and CentOS are supported for this script'
    exit 255
fi
read -p 'Press [Enter] to continue...'
echo ''
echo 'Installing...'
if [[ $HAS_PY3 -eq 0 ]]
then
    echo 'Installing Python 3...'
    $LNX_PKG_MGR install -y python3 python3-setuptools
fi
echo 'Creating application user...'
useradd -m mailguardian
echo 'Installing git commandline tools, if not available...'
$LNX_PKG_MGR install git -y
echo 'Pulling application sourcecode from GitHub...'
su - mailguardian -c 'git clone https://github.com/KHIT93/mailguardian.git /home/mailguardian/mailguardian --branch feature-new-install-scripts'
cd /home/mailguardian/mailguardian
echo 'Installing required packages...'
python3 ./installer/deps.py
usermod -a -G mtagroup,postfix mailguardian
if [ "$?" -ne 0 ]; then
    echo 'We are really sorry, but something seems to have gone wrong or the script was aborted'
    exit 1
fi
su - mailguardian -c 'cd /home/mailguardian/mailguardian && virtualenv -p python3 . && /home/mailguardian/bin/pip install -r requirements.txt'
if [ "$?" -ne 0 ]; then
    echo 'We are really sorry, but something seems to have gone wrong or the script was aborted'
    exit 1
fi
echo 'Installing MailGuardian...'
export ENV_DB_PASS=$(date +%s | sha256sum | base64 | head -c 32)
echo 'create database mailguardian;' | su - postgres -c psql
if [ "$?" -ne 0 ]; then
    echo 'We are really sorry, but something seems to have gone wrong or the script was aborted'
    exit 1
fi
echo 'create user mailguardian with encrypted password "' + $ENV_DB_PASS + '";' | su - postgres -c psql
if [ "$?" -ne 0 ]; then
    echo 'We are really sorry, but something seems to have gone wrong or the script was aborted'
    exit 1
fi
echo 'grant all privileges on database mailguardian to mailguardian;' | su - postgres -c psql
if [ "$?" -ne 0 ]; then
    echo 'We are really sorry, but something seems to have gone wrong or the script was aborted'
    exit 1
fi
bin/python ./installer/mailguardian.py
if [ "$?" -ne 0 ]; then
    echo 'We are really sorry, but something seems to have gone wrong or the script was aborted'
    exit 1
fi
echo 'Configure Postfix...'
bin/python ./installer/postfix.py
if [ "$?" -ne 0 ]; then
    echo 'We are really sorry, but something seems to have gone wrong or the script was aborted'
    exit 1
fi
echo 'Configure MailScanner...'
bin/python ./installer/mailscanner.py
if [ "$?" -ne 0 ]; then
    echo 'We are really sorry, but something seems to have gone wrong or the script was aborted'
    exit 1
fi
echo 'Installation and initial configuration completed. Now we will perform some cleanup...'
bin/python ./installer/cleanup.py
if [ "$?" -ne 0 ]; then
    echo 'We are really sorry, but something seems to have gone wrong or the script was aborted'
    exit 1
fi
echo 'Installation has finished. Please finish application configuration in your web browser'
exit 0