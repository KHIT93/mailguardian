"""
Django settings for MailGuardian project.

Generated by 'django-admin startproject' using Django 2.0.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import json
from core.helpers import MailGuardianConfiguration
from django.core.management.utils import get_random_secret_key


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MAILGUARDIAN_ENV = MailGuardianConfiguration(json.load(open(os.path.join(os.path.dirname(BASE_DIR), "mailguardian-env.json"))))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = MAILGUARDIAN_ENV.get('app_key', get_random_secret_key())
# SECURITY WARNING: keep the field encryption key used in production secret!
# We use the SECRET_KEY as a fallback for compatibility with existing installations
FIELD_ENCRYPTION_KEY = MAILGUARDIAN_ENV.get('encryption_key', None)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = MAILGUARDIAN_ENV.get("debug", False)
APP_HOSTNAME = MAILGUARDIAN_ENV.get("hostname", None)
APP_VERSION = '1.4.3'
ALLOWED_HOSTS = [APP_HOSTNAME] if APP_HOSTNAME else []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'guardian',
    'auditlog',
    'encrypted_model_fields',
    'django_premailer',
    'core',
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
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'auditlog.middleware.AuditlogMiddleware',
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
        'NAME': MAILGUARDIAN_ENV.get("database.name", 'mailguardian'),
        'USER': MAILGUARDIAN_ENV.get("database.user", 'mailguardian'),
        'PASSWORD': MAILGUARDIAN_ENV.get("database.password", 'mailguardian'),
        'HOST': MAILGUARDIAN_ENV.get("database.host", 'localhost'),
        'PORT': MAILGUARDIAN_ENV.get("database.port", ''),
        'OPTIONS': {
            'sslmode': MAILGUARDIAN_ENV.get("database.options.sslmode", 'prefer')
        },
    }
}

# Make sure that we override the databse settings when running Travis/GitLab CI
if 'TRAVIS' in os.environ or 'GITLAB_CI' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE':   'django.db.backends.postgresql',
            'NAME':     'travisci',
            'USER':     'postgres',
            'PASSWORD': '',
            'HOST':     'localhost',
            'PORT':     '',
        }
    }
elif 'GITLAB_CI' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE':   'django.db.backends.postgresql',
            'NAME':     'ci',
            'USER':     'postgres',
            'PASSWORD': 'postgres',
            'HOST':     'postgres',
            'PORT':     '5432',
        }
    }

CELERY_BROKER_URL = 'sqla+postgresql://{0}:{1}@{2}/{3}'.format(DATABASES['default']['USER'], DATABASES['default']['PASSWORD'], DATABASES['default']['HOST'], DATABASES['default']['NAME'])
CELERY_RESULT_BACKEND = 'django-db'

# Caching
# https://docs.djangoproject.com/en/2.0/topics/cache/#database-caching
if DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'path.to.backend',
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
            'LOCATION': 'cache',
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

LANGUAGE_CODE = MAILGUARDIAN_ENV.get("language_code", "en_US")

TIME_ZONE = MAILGUARDIAN_ENV.get("time_zone", "UTC")

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = [
    'locale'
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/assets/'
ASSETS_DIR = os.path.join(os.path.dirname(BASE_DIR), "assets")

if DEBUG:
    STATICFILES_DIRS = [
        os.path.join(ASSETS_DIR, "dist")
    ]
else:
    STATIC_ROOT = os.path.join(ASSETS_DIR, "dist")

# REST Framework configuration
# http://www.django-rest-framework.org/#example
REST_RENDERERS = ('rest_framework.renderers.JSONRenderer','rest_framework.renderers.BrowsableAPIRenderer',) if DEBUG else ('rest_framework.renderers.JSONRenderer',)
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication'
    ),
    'DEFAULT_PAGINATION_CLASS': 'mailguardian.pagination.PageNumberPaginationWithPageCount',
    'PAGE_SIZE': 100,
    'DEFAULT_RENDERER_CLASSES': (
        REST_RENDERERS
    )
}

REST_AUTH_SERIALIZERS = {
    'PASSWORD_RESET_SERIALIZER': 'core.serializers.MailGuardianPasswordResetSerializer'
}

# Guardian Authentication backends
# https://django-guardian.readthedocs.io/en/stable/configuration.html#configuration
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', # this is default
    'guardian.backends.ObjectPermissionBackend',
)

# Django-Premailer
PREMAILER_OPTIONS = dict(remove_classes=True)

#MailGuardian specific settings
TMP_DIR = MAILGUARDIAN_ENV.get('hostconfig.tmp_dir', '/tmp')
MTA = MAILGUARDIAN_ENV.get('mta', 'postfix')
MTA_LOGFILE = MAILGUARDIAN_ENV.get("hostconfig.mta_logfile", "/var/log/maillog")
SENDMAIL_BIN = MAILGUARDIAN_ENV.get('hostconfig.sendmail_bin', '/usr/sbin/sendmail')
AUDIT_LOGGING = MAILGUARDIAN_ENV.get('audit_log', True)
API_ONLY = MAILGUARDIAN_ENV.get('api_only_mode', False)
CONF_DIR = os.path.join(os.path.dirname(BASE_DIR), "configuration")

#MailScanner settings
MAILSCANNER_BIN = MAILGUARDIAN_ENV.get("hostconfig.mailscanner_bin", '/usr/sbin/MailScanner')
MAILSCANNER_CONFIG_DIR = MAILGUARDIAN_ENV.get("hostconfig.mailscanner_config_dir", '/etc/MailScanner')
MAILSCANNER_SHARE_DIR = MAILGUARDIAN_ENV.get("hostconfig.mailscanner_share_dir", '/usr/share/MailScanner')
MAILSCANNER_LIB_DIR = MAILGUARDIAN_ENV.get("hostconfig.mailscanner_lib_dir", '/usr/lib/MailScanner')
MAILSCANNER_QUARANTINE_DIR = MAILGUARDIAN_ENV.get("hostconfig.mailscanner_quarantine_dir", '/var/spool/MailScanner/quarantine')

# SpamAssassin settings
SALEARN_BIN = MAILGUARDIAN_ENV.get('hostconfig.salearn_bin', '/usr/bin/salearn')
SA_BIN = MAILGUARDIAN_ENV.get('hostconfig.sa_bin', '/usr/bin/spamassassin')
SA_RULES_DIR = MAILGUARDIAN_ENV.get('hostconfig.sa_rules_dir', '/usr/share/spamassassin')
SA_PREF = MAILGUARDIAN_ENV.get('hostconfig.sa_pref_file', MAILSCANNER_CONFIG_DIR+'/spamassassin.conf')

# Retention policy
RECORD_RETENTION = MAILGUARDIAN_ENV.get('retention.records', 60)
AUDIT_RETENTION = MAILGUARDIAN_ENV.get('retention.audit', 60)
QUARANTINE_RETENTION = MAILGUARDIAN_ENV.get('retention.quarantine', 60)

# Branding
BRAND_NAME = MAILGUARDIAN_ENV.get('branding.name', 'MailGuardian')
BRAND_TAGLINE = MAILGUARDIAN_ENV.get('branding.tagline', 'Securing your email')
BRAND_LOGO = MAILGUARDIAN_ENV.get('branding.logo', '')
