from fastapi import APIRouter, Depends, HTTPException, status
import uuid
from typing import Any, List, Annotated
from mailguardian.app.models.mailscanner_host import MailScannerHost
from mailguardian.app.models.user import User
from mailguardian.app.schemas.mailscanner_host import MailScannerHost as MailScannerHostSchema
from sqlmodel import Session, select
from mailguardian.app.dependencies import get_database_session, oauth2_scheme, get_current_user, requires_app_admin

router = APIRouter(
    prefix='/hosts',
    dependencies=[Depends(oauth2_scheme), Depends(requires_app_admin)],
    tags=['MailScanner Hosts']
)

# TODO: Find a way to more centrally define what is accessible
# For the initial implementation we will perform that logic in the routes directly,
# since the CLI tools are only used by admins

@router.get('', response_model=List[MailScannerHost], summary='List all MailScannerHosts', description='Returns a list of all MailScannerHosts in the system')
async def index(db: Annotated[Session, Depends(get_database_session)], authenticated_user: Annotated[User, Depends(get_current_user)]) -> List[MailScannerHost]:
    results: List[MailScannerHost] = db.exec(select(MailScannerHost)).all()
    return results

@router.post('', response_model=MailScannerHost, summary='Create a new MailScannerHost', description='Creates a new MailScannerHost in the system')
async def store(db: Annotated[Session, Depends(get_database_session)], authenticated_user: Annotated[User, Depends(get_current_user)], data: MailScannerHostSchema) -> MailScannerHost:
    res: MailScannerHost = MailScannerHost(**data.model_dump())
    db.add(res)
    db.commit()
    db.refresh(res)

    return res

@router.get('/{uuid}', response_model=MailScannerHost, summary='Output the details of a specific MailScannerHost', description='Using the UUID of a given MailScannerHost, the details of this is returned')
async def show(db: Annotated[Session, Depends(get_database_session)], authenticated_user: Annotated[User, Depends(get_current_user)], uuid: uuid.UUID) -> MailScannerHost:
    res: MailScannerHost = db.exec(select(MailScannerHost).where(MailScannerHost.uuid == uuid)).first()
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    return res

@router.put('/{uuid}', response_model=MailScannerHost, summary='Update a MailScannerHost', description='Updates the full MailScannerHost record in the system')
async def update(db: Annotated[Session, Depends(get_database_session)], authenticated_user: Annotated[User, Depends(get_current_user)], uuid: uuid.UUID, data: MailScannerHostSchema) -> MailScannerHost:
    res: MailScannerHost = db.exec(select(MailScannerHost).where(MailScannerHost.uuid == uuid)).first()
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    data: dict[str, Any] = data.model_dump()
    res.sqlmodel_update(data)
    db.add(res)
    db.commit()
    db.refresh(res)

    return res

@router.patch('/{uuid}', response_model=MailScannerHost, summary='Partial update of a MailScannerHost', description='Updates the provided fields on a MailScannerHost')
async def partial_update(db: Annotated[Session, Depends(get_database_session)], authenticated_user: Annotated[User, Depends(get_current_user)], uuid: uuid.UUID, data: MailScannerHostSchema) -> MailScannerHost:
    res: MailScannerHost = db.exec(select(MailScannerHost).where(MailScannerHost.uuid == uuid)).first()
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    data: dict[str, Any] = data.model_dump(exclude_unset=True)
    res.sqlmodel_update(data)
    db.add(res)
    db.commit()
    db.refresh(res)

    return res

@router.delete('/{uuid}', response_model=MailScannerHost, summary='Delete a MailScannerHost', description='Deletes a MailScannerHost from the system, after which we will no longer process data for it')
async def destroy(db: Annotated[Session, Depends(get_database_session)], authenticated_user: Annotated[User, Depends(get_current_user)], uuid: uuid.UUID) -> None:
    res: MailScannerHost = db.exec(select(MailScannerHost).where(MailScannerHost.uuid == uuid)).first()
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    db.delete(res)
    db.commit()