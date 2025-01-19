import pyotp
from mailguardian.config.app import RANDOM_CHARACTER_DATA
from mailguardian.app.models.user import User
from mailguardian.config.app import settings

def generate_secret() -> str:
    # return pyotp.random_base32(length=32, chars=RANDOM_CHARACTER_DATA)
    return pyotp.random_base32(length=32)

def generate_totp_url(secret: str, user: User) -> str:
    return pyotp.TOTP(s=secret, digits=6, interval=30).provisioning_uri(name=user.email, issuer_name=f'{settings.BRAND_NAME} ({settings.SERVER_HOST})', image='')

def verify_totp(secret: str, code: str) -> bool:
    totp: pyotp.TOTP = pyotp.TOTP(s=secret, digits=6, interval=30)
    return totp.now() == code