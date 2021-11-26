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
    installer_config = configparser.RawConfigParser()
    installer_config.read(args.config_file)
    PKG_MGR = installer_config['bin']['pkg']
    POSTFIX_DIR = '/etc/postfix'
    APP_DIR  = installer_config['mailguardian']['app_dir']
    # Detect the Linux distribution
    # If we can detect you specific Linux distribution,
    # we will skip the parts where we configure systemd,
    # and your webserver
    distro_data = distribution.linux_distribution(full_distribution_name=False)
    distro = distro_data[0] or 'LINUX'
    distro_version = distro_data[1] or '0'
    distro_version_codename = distro_data[2] or 'Core'
    if distro.lower() not in ['centos', 'debian', 'ubuntu', 'almalinux', 'rocky', 'rhel']:
        print('Your Linux distribution or version is not supported')
        print(distro)
        exit(255)

    conf = []
    with open(os.path.join(APP_DIR, 'perl', 'MailGuardianConf.pm'), 'r') as f:
        conf = f.readlines()
    for index, line in enumerate(conf):
        if line.strip() == "my ($db_name) = 'mailguardian';":
            conf[index] = "my ($db_name) = '{}';".format(installer_config['database']['name'])
        if line.strip() == "my ($db_host) = 'localhost';":
            conf[index] = "my ($db_host) = '{}';".format(installer_config['database']['fqdn'])
        if line.strip() == "my ($db_user) = 'mailguardian';":
            conf[index] = "my ($db_user) = '{}';".format(installer_config['database']['user'])
        if line.strip() == "my ($db_pass) = 'mailguardian';":
            conf[index] = "my ($db_pass) = '{}';".format(installer_config['database']['pass'])
    with open(os.path.join(installer_config['mailscanner']['shared'], 'perl', 'custom', 'MailGuardianConf.pm'), 'w') as f:
        f.write("\n".join(conf))
    
    os.system('ln -sf {src} {dest}'.format(src=os.path.join(APP_DIR, 'perl', 'MailGuardian.pm'), dest=os.path.join(installer_config['mailscanner']['shared'], 'perl', 'custom', 'MailGuardian.pm')))        
    os.system('ln -sf {src} {dest}'.format(src=os.path.join(APP_DIR, 'perl', 'SQLBlockAllowList.pm'), dest=os.path.join(installer_config['mailscanner']['shared'], 'perl', 'custom', 'SQLBlockAllowList.pm')))        
    os.system('ln -sf {src} {dest}'.format(src=os.path.join(APP_DIR, 'perl', 'SQLSpamSettings.pm'), dest=os.path.join(installer_config['mailscanner']['shared'], 'perl', 'custom', 'SQLSpamSettings.pm')))        
    
    conf = []
    with open(os.path.join(installer_config['mailscanner']['config'], 'MailScanner.conf'), 'r') as f:
        conf = f.readlines()

    config_control = [
        'Run As User',
        'Run As Group',
        'Detailed Spam Report',
        'Deliver Unparsable TNEF',
        'Virus Scanners',
        'Non-Forging Viruses',
        'Quarantine Whole Message',
        'Quarantine Whole Messages As Queue Files',
        'Include Scores In SpamAssassin Report',
        'Keep Spam And MCP Archive Clean',
        'Place New Headers At Top Of Message',
        'Hostname',
        'Sign Clean Messages',
        'Dont Sign HTML If Headers Exist',
        'Remove These Headers',
        'Deliver Cleaned Messages',
        'Notify Senders',
        'Disarmed Modify Subject',
        'Send Notices',
        'Is Definitely Not Spam',
        'Is Definitely Spam',
        'Definite Spam Is High Scoring',
        'Required SpamAssassin Score',
        'High SpamAssassin Score',
        'Spam Actions',
        'Non Spam Actions',
        'Log Spam',
        'Log Silent Viruses',
        'Log Dangerous HTML Tags',
        'SpamAssassin User State Di,r'
        'SpamAssassin Local State D,ir'
        'Always Looked Up Last',
        'Incoming Work User',
        'Incoming Work Group',
        'Incoming Work Permissions',
        'Quarantine User',
        'Quarantine Group',
        'Quarantine Permissions',
        'Use SpamAssassin',
        'Incoming Queue Dir',
        'Outgoing Queue Dir',
        'MTA',
        'MSMail Queue Type',
        'MSMail Delivery Method',
        'Milter Ignore Loopback',
    ]
    config_check = []
    config_add = []
    for index, line in enumerate(conf):
        if line[:11] == 'Run As User':
            config_check.append('Run As User')
            conf[index] = 'Run As User = postfix'
        if line[:12] == 'Run As Group':
            config_check.append('Run As Group')
            conf[index] = 'Run As Group = postfix'
        if line[:20] == 'Detailed Spam Report':
            config_check.append('Detailed Spam Report')
            conf[index] = 'Detailed Spam Report = yes'
        if line[:23] == 'Deliver Unparsable TNEF':
            config_check.append('Deliver Unparsable TNEF')
            conf[index] = 'Deliver Unparsable TNEF = yes'
        if line[:14] == 'Virus Scanners':
            config_check.append('Virus Scanners')
            conf[index] = 'Virus Scanners = clamd'
        if line[:19] == 'Non-Forging Viruses':
            config_check.append('Non-Forging Viruses')
            conf[index] = 'Non-Forging Viruses = Joke/ OF97/ WM97/ W97M/ eicar Zip-Password'
        if line[:24] == 'Quarantine Whole Message':
            config_check.append('Quarantine Whole Message')
            conf[index] = 'Quarantine Whole Message = yes'
        if line[:40] == 'Quarantine Whole Messages As Queue Files':
            config_check.append('Quarantine Whole Messages As Queue Files')
            conf[index] = 'Quarantine Whole Messages As Queue Files = no'
        if line[:37] == 'Include Scores In SpamAssassin Report':
            config_check.append('Include Scores In SpamAssassin Report')
            conf[index] = 'Include Scores In SpamAssassin Report = yes'
        if line[:31] == 'Keep Spam And MCP Archive Clean':
            config_check.append('Keep Spam And MCP Archive Clean')
            conf[index] = 'Keep Spam And MCP Archive Clean = yes'
        if line[:35] == 'Place New Headers At Top Of Message':
            config_check.append('Place New Headers At Top Of Message')
            conf[index] = 'Place New Headers At Top Of Message = yes'
        if line[:8] == 'Hostname':
            config_check.append('Hostname')
            conf[index] = 'Hostname = {}'.format(installer_config['mailguardian']['hostname'])
        if line[:19] == 'Sign Clean Messages':
            config_check.append('Sign Clean Messages')
            conf[index] = 'Sign Clean Messages = no'
        if line[:31] == 'Dont Sign HTML If Headers Exist':
            config_check.append('Dont Sign HTML If Headers Exist')
            conf[index] = 'Dont Sign HTML If Headers Exist = In-Reply-To: References:'
        if line[:20] == 'Remove These Headers':
            config_check.append('Remove These Headers')
            conf[index] = 'Remove These Headers = X-Mozilla-Status: X-Mozilla-Status2: Disposition-Notification-To: Return-Receipt-To:'
        if line[:24] == 'Deliver Cleaned Messages':
            config_check.append('Deliver Cleaned Messages')
            conf[index] = 'Deliver Cleaned Messages = no'
        if line[:14] == 'Notify Senders':
            config_check.append('Notify Senders')
            conf[index] = 'Notify Senders = no'
        if line[:23] == 'Disarmed Modify Subject':
            config_check.append('Disarmed Modify Subject')
            conf[index] = 'Disarmed Modify Subject = no'
        if line[:12] == 'Send Notices':
            config_check.append('Send Notices')
            conf[index] = 'Send Notices = no'
        if line[:22] == 'Is Definitely Not Spam':
            config_check.append('Is Definitely Not Spam')
            conf[index] = 'Is Definitely Not Spam = &SQLAllowlist'
        if line[:18] == 'Is Definitely Spam':
            config_check.append('Is Definitely Spam')
            conf[index] = 'Is Definitely Spam = &SQLBlocklist'
        if line[:29] == 'Definite Spam Is High Scoring':
            config_check.append('Definite Spam Is High Scoring')
            conf[index] = 'Definite Spam Is High Scoring = yes'
        if line[:27] == 'Required SpamAssassin Score':
            config_check.append('Required SpamAssassin Score')
            conf[index] = 'Required SpamAssassin Score = &SQLSpamScores'
        if line[:23] == 'High SpamAssassin Score':
            config_check.append('High SpamAssassin Score')
            conf[index] = 'High SpamAssassin Score = &SQLHighSpamScores'
        if line[:12] == 'Spam Actions':
            config_check.append('Spam Actions')
            conf[index] = 'Spam Actions = store'
        if line[:16] == 'Non Spam Actions':
            config_check.append('Non Spam Actions')
            conf[index] = 'Non Spam Actions = store deliver header "X-Spam-Status:No"'
        if line[:8] == 'Log Spam':
            config_check.append('Log Spam')
            conf[index] = 'Log Spam = yes'
        if line[:18] == 'Log Silent Viruses':
            config_check.append('Log Silent Viruses')
            conf[index] = 'Log Silent Viruses = yes'
        if line[:23] == 'Log Dangerous HTML Tags':
            config_check.append('Log Dangerous HTML Tags')
            conf[index] = 'Log Dangerous HTML Tags = yes'
        if line[:27] == 'SpamAssassin User State Dir':
            config_check.append('SpamAssassin User State Dir')
            conf[index] = 'SpamAssassin User State Dir = /var/spool/MailScanner/spamassassin'
        if line[:28] == 'SpamAssassin Local State Dir':
            config_check.append('SpamAssassin Local State Dir')
            conf[index] = 'SpamAssassin Local State Dir = /var/lib/spamassassin'
        if line[:21] == 'Always Looked Up Last':
            config_check.append('Always Looked Up Last')
            conf[index] = 'Always Looked Up Last = &MailGuardianLogging'
        if line[:18] == 'Incoming Work User':
            config_check.append('Incoming Work User')
            conf[index] = 'Incoming Work User = postfix'
        if line[:19] == 'Incoming Work Group':
            config_check.append('Incoming Work Group')
            conf[index] = 'Incoming Work Group = mtagroup'
        if line[:25] == 'Incoming Work Permissions':
            config_check.append('Incoming Work Permissions')
            conf[index] = 'Incoming Work Permissions = 0660'
        if line[:15] == 'Quarantine User':
            config_check.append('Quarantine User')
            conf[index] = 'Quarantine User = postfix'
        if line[:16] == 'Quarantine Group':
            config_check.append('Quarantine Group')
            conf[index] = 'Quarantine Group = mtagroup'
        if line[:22] == 'Quarantine Permissions':
            config_check.append('Quarantine Permissions')
            conf[index] = 'Quarantine Permissions = 0644'
        if line[:16] == 'Use SpamAssassin':
            config_check.append('Use SpamAssassin')
            conf[index] = 'Use SpamAssassin = &SQLNoScan'
        if line[:18] == 'Incoming Queue Dir':
            config_check.append('Incoming Queue Dir')
            conf[index] = 'Incoming Queue Dir = /var/spool/MailScanner/milterin'
        if line[:18] == 'Outgoing Queue Dir':
            config_check.append('Outgoing Queue Dir')
            conf[index] = 'Outgoing Queue Dir = /var/spool/MailScanner/milterout'
        if line[:3] == 'MTA':
            config_check.append('MTA')
            conf[index] = 'MTA = msmail'
        if line[:17] == 'MSMail Queue Type':
            config_check.append('MSMail Queue Type')
            conf[index] = 'MSMail Queue Type = long'
        if line[:22] == 'MSMail Delivery Method':
            config_check.append('MSMail Delivery Method')
            conf[index] = 'MSMail Delivery Method = QMQP'
        if line[:22] == 'Milter Ignore Loopback':
            config_check.append('Milter Ignore Loopback')
            conf[index] = 'Milter Ignore Loopback = no'
    for c in config_check:
        if not c in config_control:
            if 'Run As User' == c:
                conf.append('Run As User = postfix')
            if 'Run As Group' == c:
                conf.append('Run As Group = postfix')
            if 'Detailed Spam Report' == c:
                conf.append('Detailed Spam Report = yes')
            if 'Deliver Unparsable TNEF' == c:
                conf.append('Deliver Unparsable TNEF = yes')
            if 'Virus Scanners' == c:
                conf.append('Virus Scanners = clamd')
            if 'Non-Forging Viruses' == c:
                conf.append('Non-Forging Viruses = Joke/ OF97/ WM97/ W97M/ eicar Zip-Password')
            if 'Quarantine Whole Message' == c:
                conf.append('Quarantine Whole Message = yes')
            if 'Quarantine Whole Messages As Queue Files' == c:
                conf.append('Quarantine Whole Messages As Queue Files = no')
            if 'Include Scores In SpamAssassin Report' == c:
                conf.append('Include Scores In SpamAssassin Report = yes')
            if 'Keep Spam And MCP Archive Clean' == c:
                conf.append('Keep Spam And MCP Archive Clean = yes')
            if 'Place New Headers At Top Of Message' == c:
                conf.append('Place New Headers At Top Of Message = yes')
            if 'Hostname' == c:
                conf.append('Hostname = {}'.format(installer_config['mailguardian']['hostname']))
            if 'Sign Clean Messages' == c:
                conf.append('Sign Clean Messages = no')
            if 'Dont Sign HTML If Headers Exist' == c:
                conf.append('Dont Sign HTML If Headers Exist = In-Reply-To: References:')
            if 'Remove These Headers' == c:
                conf.append('Remove These Headers = X-Mozilla-Status: X-Mozilla-Status2: Disposition-Notification-To: Return-Receipt-To:')
            if 'Deliver Cleaned Messages' == c:
                conf.append('Deliver Cleaned Messages = no')
            if 'Notify Senders' == c:
                conf.append('Notify Senders = no')
            if 'Disarmed Modify Subject' == c:
                conf.append('Disarmed Modify Subject = no')
            if 'Send Notices' == c:
                conf.append('Send Notices = no')
            if 'Is Definitely Not Spam' == c:
                conf.append('Is Definitely Not Spam = &SQLAllowlist')
            if 'Is Definitely Spam' == c:
                conf.append('Is Definitely Spam = &SQLBlocklist')
            if 'Definite Spam Is High Scoring' == c:
                conf.append('Definite Spam Is High Scoring = yes')
            if 'Required SpamAssassin Score' == c:
                conf.append('Required SpamAssassin Score = &SQLSpamScores')
            if 'High SpamAssassin Score' == c:
                conf.append('High SpamAssassin Score = &SQLHighSpamScores')
            if 'Spam Actions' == c:
                conf.append('Spam Actions = store')
            if 'Non Spam Actions' == c:
                conf.append('Non Spam Actions = store deliver header "X-Spam-Status:No"')
            if 'Log Spam' == c:
                conf.append('Log Spam = yes')
            if 'Log Silent Viruses' == c:
                conf.append('Log Silent Viruses = yes')
            if 'Log Dangerous HTML Tags' == c:
                conf.append('Log Dangerous HTML Tags = yes')
            if 'SpamAssassin User State Dir' == c:
                conf.append('SpamAssassin User State Dir = /var/spool/MailScanner/spamassassin')
            if 'SpamAssassin Local State Dir' == c:
                conf.append('SpamAssassin Local State Dir = /var/lib/spamassassin')
            if 'Always Looked Up Last' == c:
                conf.append('Always Looked Up Last = &MailGuardianLogging')
            if 'Incoming Work User' == c:
                conf.append('Incoming Work User = postfix')
            if 'Incoming Work Group' == c:
                conf.append('Incoming Work Group = mtagroup')
            if 'Incoming Work Permissions' == c:
                conf.append('Incoming Work Permissions = 0660')
            if 'Quarantine User' == c:
                conf.append('Quarantine User = postfix')
            if 'Quarantine Group' == c:
                conf.append('Quarantine Group = mtagroup')
            if 'Quarantine Permissions' == c:
                conf.append('Quarantine Permissions = 0644')
            if 'Use SpamAssassin' == c:
                conf.append('Use SpamAssassin = &SQLNoScan')
            if 'Incoming Queue Dir' == c:
                conf.append('Incoming Queue Dir = /var/spool/MailScanner/milterin')
            if 'Outgoing Queue Dir' == c:
                conf.append('Outgoing Queue Dir = /var/spool/MailScanner/milterout')
            if 'MTA' == c:
                conf.append('MTA = msmail')
            if 'MSMail Queue Type' == c:
                conf.append('MSMail Queue Type = long')
            if 'MSMail Delivery Method' == c:
                conf.append('MSMail Delivery Method = QMQP')
            if 'Milter Ignore Loopback' == c:
                conf.append('Milter Ignore Loopback = no')
    with open(os.path.join(installer_config['mailscanner']['config'], 'MailScanner.conf'), 'w') as f:
        f.write("\n".join(conf))
    if not os.path.exists(os.path.join('/','var','spool','MailScanner','milterin')):
        os.makedirs(os.path.join('/','var','spool','MailScanner','milterin'))
    if not os.path.exists(os.path.join('/','var','spool','MailScanner','milterout')):
        os.makedirs(os.path.join('/','var','spool','MailScanner','milterout'))
    os.system('chown postfix:mtagroup /var/spool/MailScanner/milterin')
    os.system('chown postfix:mtagroup /var/spool/MailScanner/milterout')
    os.system('chown postfix:mtagroup /var/spool/MailScanner/incoming')
    os.system('chown postfix:mtagroup /var/spool/MailScanner/quarantine')
    os.system('echo "\nqmqp      unix  n       -       n       -       -       qmqpd" >> {postfix}/master.cf'.format(postfix=POSTFIX_DIR))
    os.system('echo "\nqmqpd_authorized_clients = 127.0.0.1" >> {postfix}/main.cf'.format(postfix=POSTFIX_DIR))
    os.system('echo "\nsmtpd_milters = inet:127.0.0.1:33333" >> {postfix}/main.cf'.format(postfix=POSTFIX_DIR))
    os.system("sed -i 's/run_mailscanner=0/run_mailscanner=1/g' /etc/MailScanner/defaults")

    if not os.path.exists('/etc/MailScanner/bayes'):
        os.system('mkdir /etc/MailScanner/bayes')
    os.system('chown postfix:mtagroup /etc/MailScanner/bayes')
    os.system('chmod g+rws /etc/MailScanner/bayes')
    if os.path.exists('/root/.spamassasin'):
        os.system('cp /root/.spamassassin/bayes_* /etc/MailScanner/bayes')
        os.system('chown postfix:mtagroup /etc/MailScanner/bayes/bayes_*')
        os.system('chmod g+rw /etc/MailScanner/bayes/bayes_*')
    
    os.system('{systemctl} enable --now msmilter.service'.format(systemctl=installer_config['bin']['systemctl']))

    if distro == 'centos':
        os.system("{sed} -i '/^Example/ c\#Example' /etc/freshclam.conf".format(sed=which('sed')))
        os.system("{sed} -i '/^Example/ c\#Example' /etc/clamd.d/scan.conf".format(sed=which('sed')))
        os.system("{sed} -i '/#LocalSocket \/run\/clamd.scan\/clamd.sock/ c\LocalSocket /var/run/clamd.scan/clamd.sock' /etc/clamd.d/scan.conf".format(sed=which('sed')))
        os.system('{chown} -R clamscan:mtagroup /var/run/clamd.scan'.format(chown=which('chown')))
        os.system('{echo} "d /var/run/clamd.scan 0750 clamscan mtagroup -" > /usr/lib/tmpfiles.d/clamd.scan.conf'.format(echo=which('echo')))
        os.system('{touch} /var/log/clamd.scan'.format(touch=which('touch')))
        os.system('{chown} clamscan:clamscan /var/log/clamd.scan'.format(chown=which('chown')))
        os.system('{usermod} -G mtagroup,virusgroup,clamupdate clamscan'.format(usermod=which('usermod')))
        os.system("{sed} -i '/#LogFile \/var\/log\/clamd.scan/ c\LogFile /var/log/clamd.scan' /etc/clamd.d/scan.conf".format(sed=which('sed')))
        os.system('{systemctl} enable clamd@scan'.format(systemctl=installer_config['bin']['systemctl']))
        os.system('{systemctl} restart clamd@scan'.format(systemctl=installer_config['bin']['systemctl']))

    if distro.lower() in ['ubuntu', 'debian']:
        os.system('{systemctl} enable clamav-daemon.service'.format(systemctl=installer_config['bin']['systemctl']))
        os.system('{systemctl} restart clamav-daemon.service'.format(systemctl=installer_config['bin']['systemctl']))
    
