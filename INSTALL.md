# Installing MailGuardian
There are generally two ways of installing MailGuardian on any of the supported Linux distributions.
 1. Using the automated installer
 2. Manually install and configure each component to your specific needs

This guide will cover the automated installation procedure, but feel free to have a look inside the install script to customize it for your needs.

## Download and run the script
Our installation script is desgined to run and install with almost no user interaction.
Simply download and run the script like this as the `root` user on your system:

```
curl https://raw.githubusercontent.com/KHIT93/mailguardian/feature-new-install-scripts/installer.sh | bash
```

During installation, the script will install `postfix` for handling incoming and outgoing email. During installation of `postfix` you will asked a couple of questions.
It is important to make sure that postfix is installed as an `Internet Site` and that you have the correct hostname set
After installing `postfix`, we need to install `PostgreSQL` and the script will ask you whether this server has to run the database or not.
If this is a single node deployment, you would generally answer this with `y` for Yes.
If you have an existing PostgreSQL installation somewhere else, then you would want to answer `n` for No
When deploying multi node, you would normally answer `y` on the node running the web UI and `n` on all other nodes

During installation, we use a tool called `cpan` to install some additional libraries needed. When this is installed, it will ask you the following question

```
Would you like to configure as much as possible automatically? [yes]
```
You can press `Enter` to select `yes`

As `cpan` will have to build some libraries from their sourcecode, the installation of these libraries can take some time. On fairly modern sytem this procedure takes 15-20 minutes.

Once all necessary tools and libraries are installed, the `MailGuardian` configuration wizard will open. This is used to configure the application to your environment
and you will asked a series of questions

```
What is the username of the user running the MailGuardian application? [mailguardian]
```
Here you simply press `Enter` to accept the default value

```
As your system will use quite a bit of space, could you please let us know how many days you want us to keep data in the system? [60]
```

By default, we have a 60 day retention policy on all data and if you wish to keep this, simply press `Enter`. Otherwise type the number of days that you
want to have instead and then press `Enter`

```
Please provide us the hostname of your PostgreSQL database server [localhost]:
```

Next we need to know the location of the database server. If you have answered yes to install the PostgreSQL server, then you can simply press `Enter` as the default value will then be the correct value.
Otherwise you need to input the hostname or IP-address of the server running PostgreSQL

```
Please provide us the username of the PostgreSQL user that has access to the database [mailguardian]:
```

Simply press `Enter` if you have answered `y` to install the PostgreSQL server. Otherwise input the username who can access the PostgreSQL database needed for MailGuardian

```
Please provide us the password for the PostgreSQL user specified above:
```

The above question will come when the database host is set to `localhost` or `127.0.0.1`

```
Please provide us the name of the PostgreSQL database [mailguardian]:
```

As the next step, we need to know the name of the database. Again press `Enter` if you have chosen to install the PostgreSQL server on this system

```
Please provide us the TCP port on which PostgreSQL is listening. To use the default port, just press Enter. Otherwise input the port:
```

If you are running the PostgreSQL server locally or using the default TCP-port 5432, then simply press `Enter`. Otherwise type in the port used for PostgreSQL

```
Please provide us with your timezone. This is usually the same as you chose during installation of your operating system. It is usually typed as Region/City. Fx. US/Eastern or Europe/Berlin
Please type in your timezone [UTC]:
```

Here you need to input your timezone. This does currently require some knowledge about how timezones work in Linux, but you normally choose this during installation of your operating system,
so the same value can be entered here.
If you do not know, then you can press `Enter` and the application will be set to use `UTC` as the timezone.

```
Please provide us with the hostname on which your MailGuardian instance will be accessible [spamfilter.example.com]:
```

The default value is not hardcoded to `spamfilter.example.com`. Instead the default value is read from the hostname property of the installed system. If you want `MailGuardian` to use this hostname
simply press `Enter`. Otherwise input the hostname and then press `Enter`

Next step is to configure the security. `MailGuardian` aims to run as secure as possible from the beginning, but without being extremely complicated.

```
Would you like to enable HTTP/2 and SSL/TLS (HTTPS) encryption for this instance? (Y/n)
```

Generally you want to answer `y` to this as it will configure a secure and encrypted connection to your installation.

```
Should this server be part of a configuration that contains multiple servers? (y/N)
```

We need to inform the script if this server is part of multi node configuration. This is to prepare certain configurations to allow for multi node. Answer `y` for multi node and `n` if you only run this one server.

If you answer `n` today and then later, want to expand the system to multiple nodes, then you can make some simple configuration changes to allow for this

```
Where are your MailScanner configuration files located? [/etc/MailScanner]
```

Normally just press `Enter` here as it is the default installation path for `MailScanner`. If you have made a custom install of `MailScanner`, please input hte path here

```
Please specify the full path to the MailScanner executable file/binary? [/usr/sbin/MailScanner]
```

Generally you can press `Enter` here, as the script has taken the default value by requesting the path of the `MailScanner` binary from the environments `$PATH`
If the suggested path is not correct, please type it in manually and press `Enter`

```
Where are the MailScanner application libraries located? [/usr/lib/MailScanner]
```

As with the previous questions about your MailScanner installation, the default is normally correct

```
Please let us know where your MailScanner shared resources are located [/usr/share/MailScanner]
```

As with the previous questions about your MailScanner installation, the default is normally correct

```
To correctly handle SPAM, could you please let us know where your 'sa-learn' binary is located? [/usr/local/bin/sa-learn]
```

As with the previous questions about the location of the MailScanner binary, the default is normally correct here is well

```
To correctly handle SPAM, could you please let us know where your 'spamassassin' binary is located? [/usr/local/bin/spamassassin]
```

As with the previous questions about the location of the MailScanner binary, the default is normally correct here is well

```
Please type in the location of your SpamAssassin rules configuration [/var/lib/spamassassin]
```

As with the previous questions about your MailScanner installation, the default is normally correct

At this point, you will be shown a summary of your settings. Answer `y` to confirm the settings.
If you need to change certain settings, it can be done afterwards or you can rerun the installation script.

```
Would you like us to automatically generate a LetsEncrypt certificate for you? (Y/n)
```

We highly recommend that you secure your installation and we will therefore offer you the option to install a valid SSL/TLS certificate
using `LetsEncrypt`. It is completely free.
Answer `y` if you would like to.
If you answer `n`, we will prompt you for usage of an existing certificate:

```
Do you want to use an existing certificate? (y/N)
```

If `y` is answered, then we will ask for the paths of the certificates.

Should you also choose to answer `n` to `Do you want to use an existing certificate? (y/N)`, then we will generate a self-signed certificate for you.
This option does techincally provide a secure and encrypted connection, but you will be prompted for trusting the certificate each time you access the installation

Once we have certificate, we will generate a set of additional security parameters to further strenghten the connection to the server.
As this is quite a long key, it can take up to 30 minutes to complete

After this has completed, the script will configure the `nginx` webserver to allow access to the application and also start the application service

The script will now configure `MailScanner` and `postfix` to work together and to work with `MailGuardian`

Once this is done, we will run some tests on `MailScanner` and `spamassassin` to ensure that they actually work
If any errors come up during the checks, you will have to fix them manually when using a custom setup. If the automated setup was used, then you are ready to go

When the installation is completely finished, it will output the password for the application user in `PostgreSQL` as you will need this when deploying multi node using the installation script

Once all your servers/nodes have been deployed, you can access the web UI using the hostname of the server, that has been configured to run the web UI