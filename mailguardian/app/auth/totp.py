import pyotp

from mailguardian.app.models.user import User
from mailguardian.config.app import settings


def generate_secret() -> str:
    """
    Generates a random base32 secret key using the specified character set.

    Returns:
        str: A 32-character long base32 encoded string.
    """
    # return pyotp.random_base32(length=32, chars=RANDOM_CHARACTER_DATA)
    return pyotp.random_base32(length=32)


def generate_totp_url(secret: str, user: User) -> str:
    """
    Generates a TOTP URL for the given secret and user.

    Parameters:
        secret (str): The base32 encoded secret key.
        user (User): The user object containing email information.

    Returns:
        str: The provisioning URI string for setting up TOTP with the given parameters.
    """
    return pyotp.TOTP(s=secret, digits=6, interval=30).provisioning_uri(name=user.email, issuer_name=f'{settings.BRAND_NAME} ({settings.SERVER_HOST})', image='')


def verify_totp(secret: str, code: str) -> bool:
    """
    Verifies the given TOTP code against the secret.

    Parameters:
        secret (str): The base32 encoded secret key.
        code (str): The 6-digit TOTP code to be verified.

    Returns:
        bool: True if the provided TOTP code matches the expected value, False otherwise.
    """
    totp: pyotp.TOTP = pyotp.TOTP(s=secret, digits=6, interval=30)
    return totp.now() == code