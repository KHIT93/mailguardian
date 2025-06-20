from datetime import timedelta, datetime, timezone
from typing import Annotated, Optional
from fastapi import Request
from injector import inject
from jose import JWTError, jwt
import logging
from passlib.context import CryptContext
import random
from sqlmodel import Session, select
import string
from mailguardian.app import services
from mailguardian.app.auth.validation import CommonPasswordValidator, MinimumLengthValidator, NumericPasswordValidator, UserAttributeSimilarityValidator, BaseValidator
from mailguardian.app.auth.totp import verify_totp
from mailguardian.app.models.audit_log import AuditLog
from mailguardian.app.models.user import User
from mailguardian.app.schemas.audit_log import AuditAction
from mailguardian.app.service_providers.dependency_injection import Depends, inject_dependencies
from mailguardian.app.utils.audit import audit_interaction
from mailguardian.config.app import settings, TOKEN_ALGORITHM, RANDOM_CHARACTER_DATA
from mailguardian.database.connect import Database

_logger = logging.getLogger(__name__)

# TODO: Find out what parameters we can define to make the usage of argon2 as secure as possible
crypt_context: CryptContext = CryptContext(schemes=['argon2'], argon2__time_cost=4, argon2__memory_cost=64*1024, argon2__parallelism=8)

def get_random_string(length: int) -> str:
    # Define list of characters to use in password
    characters: list[str] = RANDOM_CHARACTER_DATA.copy()

    # Shuffle characters randomly
    random.shuffle(characters)

    # Pick out random characters for the specified length
    password: list[str] = []
    for i in range(length):
        password.append(random.choice(characters))

    # Shuffle the selected characters again to make the password even more random
    random.shuffle(password)

    # Return the final result
    return "".join(password)


def validate_new_password(plain_password: str) -> bool:
    for validator in [CommonPasswordValidator, MinimumLengthValidator, NumericPasswordValidator, UserAttributeSimilarityValidator]:
        instance: BaseValidator = validator()
        instance.validate(password=plain_password)
    return True

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return crypt_context.verify(secret=plain_password, hash=hashed_password)

def hash_password(password: str) -> str:
    return crypt_context.hash(secret=password)


@inject_dependencies()
def authenticate_user(db: Annotated[Database, Depends()], request: Request, username: str, password: str, verification_code: Optional[str] = '') -> User | bool:
    db_session: Session = db.get_session()
    user: User = db_session.exec(select(User).where(User.email == username and User.is_active == True)).first()

    if not user:
        _logger.info('No valid user found')
        audit_interaction(
            request=request,
            action=AuditAction.LOGIN,
            model=User.__name__,
            res_id=None,
            actor_id=None,
            message=f'Denied login as {username}. User does not exist or is inactive',
            allowed=False
        )
        _logger.error('No active user found')
        return False

    _logger.info(f'Found user with email {username}')
    
    if not verify_password(plain_password=password, hashed_password=user.password):
        audit_interaction(
            action=AuditAction.LOGIN,
            model=User.__name__,
            res_id=user.id,
            actor_id=None,
            message=f'Denied login as {username}. Incorrect credentials',
            allowed=False
        )
        _logger.error(f'Could not log in user with email {username} as the password is incorrect')
        return False
    if user.totp_codes:
        if not any(verify_totp(totp.totp_secret, verification_code) for totp in user.totp_codes):
            audit_interaction(
                action=AuditAction.LOGIN,
                model=User.__name__,
                res_id=user.id,
                actor_id=None,
                message=f'Denied login as {username}. Incorrect 2FA',
                allowed=False
            )
            db_session.commit()
            _logger.error(f'Could not log in user with email {username} as the 2FA verification code is invalid')
            return False
    audit_interaction(
        action=AuditAction.LOGIN,
        model=User.__name__,
        res_id=user.id,
        actor_id=None,
        message=f'Authenticated login as {username}.',
        allowed=True
    )
    db_session.commit()
    _logger.info(f'User {username} has authenticated')
    return user
    
def create_access_token(data: dict, expires_delta: timedelta | None) -> str:
    to_encode: dict = data.copy()
    expire: datetime = datetime.now(timezone.utc) + timedelta(minutes=15)
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta

    to_encode.update({'exp': expire})

    encoded_jwt = jwt.encode(claims=to_encode, key=settings.SECRET_KEY, algorithm=TOKEN_ALGORITHM)

    return encoded_jwt

