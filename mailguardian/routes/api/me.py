from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlmodel import Session, delete, select

from mailguardian.app.auth.utils import hash_password, validate_new_password, verify_password
from mailguardian.app.dependencies import (
    get_current_token,
    get_current_user,
    get_database_session,
    oauth2_scheme,
)
from mailguardian.app.models.audit_log import AuditLog
from mailguardian.app.models.domain import Domain
from mailguardian.app.models.user import User, UserSession
from mailguardian.app.schemas.audit_log import AuditAction
from mailguardian.app.schemas.user import ChangePassword, PersonalDetails, TokenData, UserRole

router = APIRouter(
    prefix='/me',
    dependencies=[Depends(oauth2_scheme)],
    tags=['Account Management']
)


@router.get('/personal', summary='Fetch details about yourself', description='Returns details required to show and update information about your user account')
async def get_personal_details(authenticated_user: Annotated[User, Depends(get_current_user)]) -> PersonalDetails:
    return authenticated_user


@router.post('/personal', summary='Updates details about yourself', description='Updates details about your self in your account')
async def update_personal_details(db: Annotated[Session, Depends(get_database_session)], authenticated_user: Annotated[User, Depends(get_current_user)], data: PersonalDetails) -> PersonalDetails:
    user: User = db.exec(select(User.id == authenticated_user.id))
    user.sqlmodel_update(data)
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.get('/domains', summary='Fetch domains you have access to', description='Returns a list of domains that you have access to')
async def get_domains(db: Annotated[Session, Depends(get_database_session)], authenticated_user: Annotated[User, Depends(get_current_user)]) -> list[Domain]:
    if authenticated_user.role == UserRole.DOMAIN_ADMINISTRATOR:
        return authenticated_user.domains
    elif authenticated_user.role == UserRole.SUPERUSER:
        return db.exec(select(Domain)).fetchmany(10)
    else:
        return []

@router.delete('/sessions', summary='Terminate all sessions for the current user', description='Call this endpoint to terminate all sessions/tokens for the current user and effectively require the user to log in again')
async def terminate_sessions(db: Annotated[Session, Depends(get_database_session)], request: Request, authenticated_user: Annotated[User, Depends(get_current_user)]) -> None:
    sessions: list[UserSession] = db.exec(delete(UserSession).where(UserSession.user_id == authenticated_user.id))
    
    
    db.add(AuditLog(
        action=AuditAction.DELETE,
        model=User.__name__,
        res_id=authenticated_user.id,
        actor_id=authenticated_user.id,
        acted_from=request.client.host,
        message=f'Invalidated all sessions for {authenticated_user.email}')
    )

    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.post('/password/change', summary='Change your password', description='Changes the password of the currently logged in user')
async def change_password(db: Annotated[Session, Depends(get_database_session)], request: Request, authenticated_user: Annotated[User, Depends(get_current_user)], token: Annotated[TokenData, Depends(get_current_token)], data: ChangePassword) -> None:
    if not verify_password(data.current_password, authenticated_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials. Change of password has been denied')

    if not data.password == data.confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Entered passwords do not match. Please ensure that they match and try again')
    
    validate_new_password(data.password)

    new_password: str = hash_password(data.password)
    if new_password == authenticated_user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='You cannot set your current password as the new one')

    authenticated_user.password = new_password

    db.add(authenticated_user)

    db.add(AuditLog(
        action=AuditAction.DELETE,
        model=User.__name__,
        res_id=authenticated_user.id,
        actor_id=authenticated_user.id,
        acted_from=request.client.host,
        message=f'{authenticated_user.email} changed their password')
    )

    if data.terminate_sessions:
        db.exec(delete(UserSession).where(UserSession.user_id == authenticated_user.id).where(UserSession.uuid != token.session_id))

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)