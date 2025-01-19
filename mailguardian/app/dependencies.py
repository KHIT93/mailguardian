from typing import Annotated, Any
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from mailguardian.app.models.user import User, UserSession
from mailguardian.app.schemas.user import TokenData, UserRole
from mailguardian.config.app import settings, TOKEN_ALGORITHM
from mailguardian.database.connect import engine
from sqlmodel import create_engine, SQLModel, Session, select
import logging

logger = logging.getLogger(__name__)

def get_database_session():
    with Session(engine) as session:
        yield session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')

async def get_current_token(token: Annotated[str, Depends(oauth2_scheme)]) -> TokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data: TokenData = None

    try:
        payload = jwt.decode(token=token, key=settings.SECRET_KEY, algorithms=[TOKEN_ALGORITHM])
        token_data = TokenData(username=payload.get('sub'), session_id=payload.get('sessId'))
    except JWTError:
        raise credentials_exception
    
    return token_data

async def get_current_user(token: Annotated[TokenData, Depends(get_current_token)]) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # payload: dict[str, Any] = {}
    # username: str = ''

    # try:
    #     payload = jwt.decode(token=token, key=settings.SECRET_KEY, algorithms=[TOKEN_ALGORITHM])
    #     username = payload.get('sub')
    #     if not username:
    #         raise credentials_exception
        
    #     token_data = TokenData(username=username, session_id=payload.get('sessId'))

    # except JWTError:
    #     raise credentials_exception
    
    with Session(engine) as db:
        user: User = db.exec(select(User).where(User.email == token.username and User.is_active == True)).first()
        if not user:
            raise credentials_exception
        
        user_session: UserSession = db.exec(select(UserSession).where(UserSession.user_id == user.id).where(UserSession.uuid == token.session_id)).first()

        if not user_session:
            raise credentials_exception

        return user
    
async def requires_app_admin(user: Annotated[User, Depends(get_current_user)]) -> bool:
    if not user.role == UserRole.SUPERUSER:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    return True