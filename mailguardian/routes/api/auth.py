from datetime import timedelta
import logging
from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlmodel import Session, select
from mailguardian.app.dependencies import get_current_user, get_database_session
from mailguardian.app.auth.utils import authenticate_user, create_access_token
from mailguardian.app.auth.providers import OAuth2MfaPasswordRequestForm
from mailguardian.app.dependencies import oauth2_scheme
from mailguardian.app.models.audit_log import AuditLog
from mailguardian.app.models.user import User
from mailguardian.app.schemas.audit_log import AuditAction
from mailguardian.app.schemas.user import Token
from mailguardian.config.app import settings

_logger = logging.getLogger(__name__)

if settings.APP_ENFORCE_MFA:
    from mailguardian.app.auth.providers import OAuth2MfaPasswordRequestForm as OAutu2PasswordRequest
else:
    from fastapi.security import OAuth2PasswordRequestForm as OAutu2PasswordRequest

router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)

@router.post('/token')
async def login(form_data: Annotated[OAutu2PasswordRequest, Depends()], request: Request, db: Annotated[Session, Depends(get_database_session)]) -> Token:
    user: User = authenticate_user(request=request, db=db, username=form_data.username, password=form_data.password)
    # TODO: Verify 2FA code

    if not user:
        _logger.error('No active user was found with username %s' % (form_data.username,))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='No account was found with the provided credentials'
        )
    db.refresh(user)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    db.add(AuditLog(
        action=AuditAction.LOGIN,
        model=User.__name__,
        res_id=user.id,
        actor_id=None,
        acted_from=request.client.host,
        message='Logged %s in.' % (form_data.username,))
    )
    db.commit()
    return Token(access_token=access_token, token_type="bearer")

@router.get('/whoami', dependencies=[Depends(oauth2_scheme)])
async def session(authenticated_user: Annotated[User, Depends(get_current_user)]) -> User:
    return authenticated_user

@router.get('/params', summary='Authentication Parameters', description='Endpoint used by clients to determine what specific authentication options are supported')
async def auth_params() -> List[str]:
    return [
        'password',
        'mfa',
        'email',
        'passkey'
    ]