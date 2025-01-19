import datetime
from typing import Annotated, Any
import uuid

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlmodel import Session, delete, select

from mailguardian.app.auth.totp import (
    generate_secret,
    generate_totp_url,
    verify_totp
)
from mailguardian.app.auth.utils import verify_password
from mailguardian.app.dependencies import (
    get_current_user,
    get_database_session,
    oauth2_scheme,
)
from mailguardian.app.models.user import User, TimeBasedCode
from mailguardian.app.schemas.audit_log import AuditAction
from mailguardian.app.schemas.user import TotpSetup, TotpSetupVerification
from mailguardian.app.utils.audit import audit_interaction

router = APIRouter(
    prefix='/totp',
    dependencies=[Depends(oauth2_scheme)],
    tags=['TOTP']
)

@router.get('/status', summary='Check TOTP Status', description='This endpoint returns a boolean indicator for whether or not TOTP-based 2FA is enabled or not')
def get_totp_status(authenticated_user: Annotated[User, Depends(get_current_user)]) -> bool:
    return bool(len(authenticated_user.totp_codes))

@router.get('/devices', summary='Shows configured devices/apps for TOTP', description='Returns a list of the devices/apps configured for TOTP codes on the current user')
def get_totp_devices(db: Annotated[Session, Depends(get_database_session)], request: Request, authenticated_user: Annotated[User, Depends(get_current_user)]) -> list[TimeBasedCode]:
    current_user: User = db.exec(select(User).where(User.id == authenticated_user.id)).first()
    audit_interaction(db=db, request=request, action=AuditAction.READ, model=TimeBasedCode.__name__, res_id=authenticated_user.id, actor_id=authenticated_user.id, message=f'Fetched TOTP Codes')
    return current_user.totp_codes

@router.delete('/devices/{id}', summary='Revoke a TOTP device/app', description='Removes an assigned TOTP device/app from the current user to make it invalid')
def delete_totp_device(db: Annotated[Session, Depends(get_database_session)], request: Request, authenticated_user: Annotated[User, Depends(get_current_user)], id: uuid.UUID) -> bool:
    totp_code: TimeBasedCode = db.exec(select(TimeBasedCode).where(TimeBasedCode.uuid == id)).first()
    if not totp_code:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    totp_name: str = totp_code.name
    db.delete(totp_code)
    db.commit()
    audit_interaction(db=db, request=request, action=AuditAction.DELETE, model=TimeBasedCode.__name__, res_id=authenticated_user.id, actor_id=authenticated_user.id, message=f'Revoked TOTP Code for {totp_name}')
    return True

@router.post('/enable', summary='Enable 2FA with TOTP', description='Enable the TOTP-based 2FA for your user')
def enable_totp(db: Annotated[Session, Depends(get_database_session)], request: Request, authenticated_user: Annotated[User, Depends(get_current_user)]) -> TotpSetup:
    audit_interaction(db=db, request=request, action=AuditAction.CREATE, model=User.__name__, res_id=authenticated_user.id, actor_id=authenticated_user.id, message=f'Started TOTP setup for {authenticated_user.email} [ID: {authenticated_user.id}]')

    secret: str = generate_secret()
    setup: TotpSetup = TotpSetup(secret=secret, url=generate_totp_url(secret=secret, user=authenticated_user))

    return setup

@router.post('/enable/confirm', summary='Confirm and verify TOTP setup', description='Handles verification of generated TOTP and confirms that it has to be enabled')
def confirm_enable_totp(db: Annotated[Session, Depends(get_database_session)], request: Request, authenticated_user: Annotated[User, Depends(get_current_user)], data: TotpSetupVerification) -> bool:
    # First verify the users current password, just to ensure that they actually know it and that we do not have some kind of hijacked JWT
    if not verify_password(plain_password=data.password, hashed_password=authenticated_user.password):
        audit_interaction(db=db, request=request, action=AuditAction.LOGIN, model=User.__name__, actor_id=authenticated_user.id, message=f'Setup of TOTP for {authenticated_user.email} [ID: {authenticated_user.id}] has failed, due to an invalid password')
        raise HTTPException(
            detail='Setup failed. Invalid credentials',
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    # Verify if the user device
    if not verify_totp(secret=data.secret, code=data.code):
        audit_interaction(db=db, request=request, action=AuditAction.LOGIN, model=User.__name__, actor_id=authenticated_user.id, message=f'Setup of TOTP for {authenticated_user.email} [ID: {authenticated_user.id}] has failed, due to an invalid verification code')
        raise HTTPException(
            detail='Setup failed. Invalid verification code',
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    res: TimeBasedCode = TimeBasedCode(user_id=authenticated_user.id, totp_secret=data.secret, name=data.name, created_at=datetime.datetime.now(datetime.timezone.utc))
    db.add(res)
    db.commit()
    db.refresh(res)

    return True