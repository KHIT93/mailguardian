# Mailware
A Django-based RESTful SPA web GUI for MailScanner

## Getting started

### Prepare MailScanner config on postfix after install

```
mkdir -p /var/spool/MailScanner/spamassassin/
chown -R postfix:mtagroup /var/spool/MailScanner/spamassassin
chown -R postfix:postfix /var/spool/MailScanner/incoming
chown -R postfix:postfix /var/spool/MailScanner/quarantine
chmod -R g+r /var/spool/postfix/{hold,incoming}
usermod -a -G mtagroup mailware
apt install postgresqlXX-server-dev libpq-dev libdata-dumper-simple-perl libpng-dev
cpan -i CPAN
cpan -i Data::Dumper
cpan -i Data::UUID
cpan -i DBI
cpan -i DBD::Pg
cpan -i Encoding::FixLatin
cpan -i Digest::SHA1
cpan -i Mail::ClamAV
cpan -i SAVI
mkdir /etc/MailScanner/bayes
chown root:mtagroup /etc/MailScanner/bayes
chmod g+rws /etc/MailScanner/bayes
```


```
$ sudo certbot certonly --authenticator standalone --pre-hook "systemctl stop nginx" --post-hook "systemctl start nginx"
```

```
0 0,12 * * * python -c 'import random; import time; time.sleep(random.random() * 3600)' && certbot renew 
```