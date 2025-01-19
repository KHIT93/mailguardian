import logging
from datetime import timedelta, datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlmodel import Session, select

from mailguardian.app.auth.utils import authenticate_user, create_access_token
from mailguardian.app.dependencies import (
    get_current_token,
    get_current_user,
    get_database_session,
    oauth2_scheme,
)
from mailguardian.app.models.audit_log import AuditLog
from mailguardian.app.models.user import User, UserSession
from mailguardian.app.schemas.audit_log import AuditAction
from mailguardian.app.schemas.auth import AuthenticationParameters, AuthenticationRequest
from mailguardian.app.schemas.user import Token, TokenData
from mailguardian.config.app import settings

_logger = logging.getLogger(__name__)

from mailguardian.app.auth.providers import (
    OAuth2MfaPasswordRequestForm as OAuth2PasswordRequest,
)


router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)


@router.post('/token')
async def login(form_data: Annotated[OAuth2PasswordRequest, Depends()], request: Request, db: Annotated[Session, Depends(get_database_session)]) -> Token:
    user: User = authenticate_user(request=request, db=db, username=form_data.username, password=form_data.password, verification_code=form_data.verification_code)
    # TODO: Verify 2FA code

    if not user:
        _logger.error(f'No active user was found with username {form_data.username}')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='No account was found with the provided credentials'
        )
    db.refresh(user)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    user_session: UserSession = UserSession(user=user, expires_at=datetime.now(timezone.utc) + access_token_expires)
    db.add(user_session)

    access_token = create_access_token(
        data={"sub": user.email, "sessId": str(user_session.uuid)}, expires_delta=access_token_expires
    )
    db.add(AuditLog(
        action=AuditAction.LOGIN,
        model=User.__name__,
        res_id=user.id,
        actor_id=None,
        acted_from=request.client.host,
        message=f'Logged {form_data.username} in.')
    )
    db.commit()
    return Token(access_token=access_token, token_type="bearer")


@router.get('/whoami', dependencies=[Depends(oauth2_scheme)])
async def session(authenticated_user: Annotated[User, Depends(get_current_user)], token: Annotated[TokenData, Depends(get_current_token)]) -> User:
    return authenticated_user

@router.delete('/terminate', dependencies=[Depends(oauth2_scheme)])
async def logout(db: Annotated[Session, Depends(get_database_session)], request: Request, authenticated_user: Annotated[User, Depends(get_current_user)], token: Annotated[TokenData, Depends(get_current_token)]) -> None:
    user_session: UserSession = db.exec(select(UserSession).where(UserSession.uuid == token.session_id, UserSession.user_id == authenticated_user.id)).first()
    db.delete(user_session)

    db.add(AuditLog(
        action=AuditAction.LOGOUT,
        model=User.__name__,
        res_id=authenticated_user.id,
        actor_id=authenticated_user.id,
        acted_from=request.client.host,
        message=f'Logged {authenticated_user.email} out.')
    )

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.post('/params', summary='Authentication Parameters', description='Endpoint used by clients to determine what specific authentication options are supported')
async def auth_params(db: Annotated[Session, Depends(get_database_session)], data: AuthenticationRequest) -> AuthenticationParameters:
    attempted_user: User = db.exec(select(User).where(User.email == data.username and User.is_active == True)).first()

    if not attempted_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with email {data.username} could not be found')

    params: AuthenticationParameters = AuthenticationParameters(password=bool(attempted_user.password), mfa=bool(len(attempted_user.totp_codes)), passkey=False, email=False)

    return params
