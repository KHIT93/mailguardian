from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import Depends, Request
from jose import JWTError, jwt
import logging
from passlib.context import CryptContext
import random
from sqlmodel import Session, select
import string
from mailguardian.app.auth.validation import CommonPasswordValidator, MinimumLengthValidator, NumericPasswordValidator, UserAttributeSimilarityValidator, BaseValidator
from mailguardian.app.dependencies import get_database_session
from mailguardian.app.models.audit_log import AuditLog
from mailguardian.app.models.user import User
from mailguardian.app.schemas.audit_log import AuditAction
from mailguardian.config.app import settings, TOKEN_ALGORITHM
from mailguardian.database.connect import engine


RANDOM_CHARACTER_DATA: list[str] = list(string.ascii_letters + string.digits + string.punctuation.replace('"','').replace('\'',''))

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

# TODO: Find out what parameters we can define to make the usage of argon2 as secure as possible
crypt_context: CryptContext = CryptContext(schemes=['argon2'])

def validate_new_password(plain_password: str) -> bool:
    for validator in [CommonPasswordValidator, MinimumLengthValidator, NumericPasswordValidator, UserAttributeSimilarityValidator]:
        instance: BaseValidator = validator()
        instance.validate(password=plain_password)
    return True

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return crypt_context.verify(secret=plain_password, hash=hashed_password)

def hash_password(password: str) -> str:
    # return crypt_context.using(time_cost=3, memory_cost=102400, max_threads=8).hash(secret=password)
    return crypt_context.hash(secret=password)

_logger = logging.getLogger(__name__)
def authenticate_user(request: Request, db: Annotated[Session, Depends(get_database_session)], username: str, password: str) -> User | bool:
    # with Session(engine) as db:
    user: User = db.exec(select(User).where(User.email == username and User.is_active == True)).first()

    if not user:
        _logger.info('No valid user found')
        db.add(AuditLog(
            action=AuditAction.LOGIN,
            model=User.__name__,
            res_id=None,
            actor_id=None,
            acted_from=request.client.host,
            message='Denied login as %s. User does not exist or is inactive' % (username,)),
            allowed=False
        )
        db.commit()
        _logger.error('No active user found')
        return False

    _logger.info('Found user with email %s' % (username,))
    
    if not verify_password(plain_password=password, hashed_password=user.password):
        db.add(AuditLog(
            action=AuditAction.LOGIN,
            model=User.__name__,
            res_id=user.id,
            actor_id=None,
            acted_from=request.client.host,
            message='Denied login as %s. Incorrect credentials' % (username,)),
            allowed=False
        )
        db.commit()
        _logger.error('Could not log in user with email %s as the password is incorrect' % (username,))
        return False
    db.add(AuditLog(
        action=AuditAction.LOGIN,
        model=User.__name__,
        res_id=user.id,
        actor_id=None,
        acted_from=request.client.host,
        message='Authenticated login as %s.' % (username,)),
        allowed=True
    )
    db.commit()
    _logger.info('User %s has authenticated' % (username,))
    return user
    
def create_access_token(data: dict, expires_delta: timedelta | None) -> str:
    to_encode: dict = data.copy()
    expire: datetime = datetime.now(timezone.utc) + timedelta(minutes=15)
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta

    to_encode.update({'exp': expire})

    encoded_jwt = jwt.encode(claims=to_encode, key=settings.SECRET_KEY, algorithm=TOKEN_ALGORITHM)

    return encoded_jwt