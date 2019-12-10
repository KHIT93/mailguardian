from .core_settings import *
from .local import *

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

# try:
#     from .local import *
# except:
#     pass