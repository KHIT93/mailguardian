import cryptography.fernet
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

def get_crypter():
    configured_keys = getattr(settings, 'FIELD_ENCRYPTION_KEY', None)

    if configured_keys is None:
        raise ImproperlyConfigured('FIELD_ENCRYPTION_KEY must be defined in settings')

    try:
        # Allow the use of key rotation
        if isinstance(configured_keys, (tuple, list)):
            keys = [parse_key(k) for k in configured_keys]
        else:
            # else turn the single key into a list of one
            keys = [parse_key(configured_keys), ]
    except Exception as e:
        raise ImproperlyConfigured('FIELD_ENCRYPTION_KEY defined incorrectly: {}'.format(str(e)))

    if len(keys) == 0:
        raise ImproperlyConfigured('No keys defined in setting FIELD_ENCRYPTION_KEY')

    return cryptography.fernet.MultiFernet(keys)

CRYPTER = get_crypter()


def encrypt_str(s):
    # be sure to encode the string to bytes
    return CRYPTER.encrypt(s.encode('utf-8'))


def decrypt_str(t):
    # be sure to decode the bytes to a string
    return CRYPTER.decrypt(t.encode('utf-8')).decode('utf-8')
