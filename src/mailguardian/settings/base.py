"""
Django settings for MailGuardian project.

Generated by 'django-admin startproject' using Django 2.0.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import platform
from pathlib import Path
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'UNSECURE_SECRET_KEY'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
APP_HOSTNAME = platform.node()
APP_VERSION = '3.0.0'
LOCAL_CONFIG_VERSION = '0.0.0'
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'trench',
    'core',
    'compliance',
    'frontend',
    'setup_wizard',
    'domains',
    'mail',
    'spamassassin',
    'lists',
    'reports',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'compliance.middleware.DataLogMiddleware',
]

ROOT_URLCONF = 'mailguardian.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mailguardian.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mailguardian',
        'USER': 'mailguardian',
        'PASSWORD': 'mailguardian',
        'HOST': 'localhost',
        'PORT': '',
        'OPTIONS': {
            'sslmode': 'prefer'
        },
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'core.User'
OLD_PASSWORD_FIELD_ENABLED = True

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
]

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

LOCALE_PATHS = [
    'locale'
]

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/assets/'
ASSETS_DIR = Path(BASE_DIR.parent, 'assets')

# Guardian Authentication backends
# https://django-guardian.readthedocs.io/en/stable/configuration.html#configuration
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', # this is default
)

# https://django-rest-auth.readthedocs.io/en/latest/configuration.html#configuration
REST_AUTH = {
    'USER_DETAILS_SERIALIZER': 'core.serializers.AccountUserSerializer',
    'PASSWORD_RESET_SERIALIZER': 'core.serializers.MailGuardianPasswordResetSerializer'
}

TRENCH_AUTH = {
    "BACKUP_CODES_QUANTITY": 6,
    "BACKUP_CODES_LENGTH": 24,
    "ENCRYPT_BACKUP_CODES": True, # This is the default setting in django-trench, but we set it explicitly here to encrypt codes if the default changes
    "SECRET_KEY_LENGTH": 64,
    "DEFAULT_VALIDITY_PERIOD": 30,
    "APPLICATION_ISSUER_NAME": 'MailGuardian',
    "MFA_METHODS": {
        "email": {
            "VERBOSE_NAME": _("email"),
            "VALIDITY_PERIOD": 60 * 5, # Default code validity is 
            "HANDLER": "trench.backends.basic_mail.SendMailMessageDispatcher",
            "SOURCE_FIELD": "username",
            "EMAIL_SUBJECT": _("Your verification code"),
            "EMAIL_PLAIN_TEMPLATE": "trench/backends/email/code.txt",
            "EMAIL_HTML_TEMPLATE": "trench/backends/email/code.html",
        },
        "app": {
            "VERBOSE_NAME": _("app"),
            "VALIDITY_PERIOD": 30,
            "USES_THIRD_PARTY_CLIENT": True,
            "HANDLER": "trench.backends.application.ApplicationMessageDispatcher",
        },
    }
}

# Django-Premailer
PREMAILER_OPTIONS = dict(remove_classes=True)

#MailGuardian specific settings
TMP_DIR = '/tmp'
MTA = 'postfix'
MTA_LOGFILE = '/var/log/maillog'
SENDMAIL_BIN = '/usr/sbin/sendmail'
POSTQUEUE_BIN = '/usr/sbin/postqueue'
AUDIT_LOGGING = True
API_ONLY = False
CONF_DIR = Path(BASE_DIR.parent, "configuration")

#MailScanner settings
MAILSCANNER_BIN = '/usr/sbin/MailScanner'
MAILSCANNER_CONFIG_DIR = '/etc/MailScanner'
MAILSCANNER_SHARE_DIR = '/usr/share/MailScanner'
MAILSCANNER_LIB_DIR = '/usr/lib/MailScanner'
MAILSCANNER_QUARANTINE_DIR = '/var/spool/MailScanner/quarantine'

# SpamAssassin settings
SALEARN_BIN = '/usr/bin/salearn'
SA_BIN = '/usr/bin/spamassassin'
SA_RULES_DIR = '/usr/share/spamassassin'
SA_PREF = MAILSCANNER_CONFIG_DIR+'/spamassassin.conf'

# Retention policy
RECORD_RETENTION = 60
AUDIT_RETENTION = 60
QUARANTINE_RETENTION = 60

# Branding
BRAND_NAME = 'MailGuardian'
BRAND_TAGLINE = 'Securing your email'
BRAND_LOGO = ''
BRAND_SUPPORT = 'https://github.com/khit93/mailguardian/issues'
BRAND_FEEDBACK = 'https://github.com/khit93/mailguardian/issues'

# GeoIP
MAXMIND_DB_PATH = Path(BASE_DIR.parent, 'run')
MAXMIND_DB_FILE = Path(MAXMIND_DB_PATH, 'GeoLite2.mmdb')
MAXMIND_ACCOUNT_API_KEY = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

CORS_ALLOW_ALL_ORIGINS = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 60
SECURE_SSL_REDIRECT = True
SECURE_HSTS_INCLUDE_SUBDOMAINS  = True
SECURE_HSTS_PRELOAD = True