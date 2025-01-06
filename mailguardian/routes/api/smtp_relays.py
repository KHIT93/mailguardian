import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from mailguardian.app.dependencies import (
    get_database_session,
    oauth2_scheme,
    requires_app_admin,
)
from mailguardian.app.models.smtp_relay import SmtpRelay
from mailguardian.app.schemas.smtp_relay import SmtpRelay as SmtpRelaySchema

router = APIRouter(
    prefix='/relays',
    dependencies=[Depends(oauth2_scheme), Depends(requires_app_admin)],
    tags=['Email Relays']
)

# TODO: Find a way to more centrally define what is accessible
# For the initial implementation we will perform that logic in the routes directly,
# since the CLI tools are only used by admins


@router.get('', summary='List all SmtpRelays', description='Returns a list of all SmtpRelays in the system')
async def index(db: Annotated[Session, Depends(get_database_session)]) -> list[SmtpRelay]:
    results: list[SmtpRelay] = db.exec(select(SmtpRelay)).all()
    return results


@router.post('', summary='Create a new SmtpRelay', description='Creates a new SmtpRelay in the system')
async def store(db: Annotated[Session, Depends(get_database_session)], data: SmtpRelaySchema) -> SmtpRelay:
    res: SmtpRelay = SmtpRelay(**data.model_dump())
    db.add(res)
    db.commit()
    db.refresh(res)

    return res


@router.get('/{id}', summary='Output the details of a specific SmtpRelay', description='Using the UUID of a given SmtpRelay, the details of this is returned')
async def show(db: Annotated[Session, Depends(get_database_session)], id: uuid.UUID) -> SmtpRelay:
    res: SmtpRelay = db.exec(select(SmtpRelay).where(SmtpRelay.uuid == id)).first()
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    return res


@router.put('/{id}', summary='Update a SmtpRelay', description='Updates the full SmtpRelay record in the system')
async def update(db: Annotated[Session, Depends(get_database_session)], id: uuid.UUID, data: SmtpRelaySchema) -> SmtpRelay:
    res: SmtpRelay = db.exec(select(SmtpRelay).where(SmtpRelay.uuid == id)).first()
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


@router.patch('/{id}', summary='Partial update of a SmtpRelay', description='Updates the provided fields on a SmtpRelay')
async def partial_update(db: Annotated[Session, Depends(get_database_session)], id: uuid.UUID, data: SmtpRelaySchema) -> SmtpRelay:
    res: SmtpRelay = db.exec(select(SmtpRelay).where(SmtpRelay.uuid == id)).first()
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


@router.delete('/{id}', response_model=SmtpRelay, summary='Delete a SmtpRelay', description='Deletes a SmtpRelay from the system, after which we will no longer process data for it')
async def destroy(db: Annotated[Session, Depends(get_database_session)], id: uuid.UUID) -> None:
    res: SmtpRelay = db.exec(select(SmtpRelay).where(SmtpRelay.uuid == id)).first()
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    db.delete(res)
    db.commit()
