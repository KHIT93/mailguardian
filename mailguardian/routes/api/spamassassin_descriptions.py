import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from mailguardian.app.dependencies import (
    get_database_session,
    oauth2_scheme,
    requires_app_admin,
)
from mailguardian.app.models.spamassassin_rule_description import (
    SpamAssassinRuleDescription,
)
from mailguardian.app.schemas.spamassassin_rule_description import (
    SpamAssassinRuleDescription as SpamAssassinRuleDescriptionSchema,
)

router = APIRouter(
    prefix='/spamassassin/descriptions',
    dependencies=[Depends(oauth2_scheme), Depends(requires_app_admin)],
    tags=['SpamAssassin Rules']
)

# TODO: Find a way to more centrally define what is accessible
# For the initial implementation we will perform that logic in the routes directly,
# since the CLI tools are only used by admins


@router.get('', summary='List all SpamAssassinRuleDescriptions', description='Returns a list of all SpamAssassinRuleDescriptions in the system')
async def index(db: Annotated[Session, Depends(get_database_session)]) -> list[SpamAssassinRuleDescription]:
    results: list[SpamAssassinRuleDescription] = db.exec(select(SpamAssassinRuleDescription)).all()
    return results


@router.post('', summary='Create a new SpamAssassinRuleDescription', description='Creates a new SpamAssassinRuleDescription in the system')
async def store(db: Annotated[Session, Depends(get_database_session)], data: SpamAssassinRuleDescriptionSchema) -> SpamAssassinRuleDescription:
    res: SpamAssassinRuleDescription = SpamAssassinRuleDescription(**data.model_dump())
    db.add(res)
    db.commit()
    db.refresh(res)

    return res


@router.get('/{id}', summary='Output the details of a specific SpamAssassinRuleDescription', description='Using the UUID of a given SpamAssassinRuleDescription, the details of this is returned')
async def show(db: Annotated[Session, Depends(get_database_session)], id: uuid.UUID) -> SpamAssassinRuleDescription:
    res: SpamAssassinRuleDescription = db.exec(select(SpamAssassinRuleDescription).where(SpamAssassinRuleDescription.uuid == id)).first()
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    return res


@router.put('/{id}', summary='Update a SpamAssassinRuleDescription', description='Updates the full SpamAssassinRuleDescription record in the system')
async def update(db: Annotated[Session, Depends(get_database_session)], id: uuid.UUID, data: SpamAssassinRuleDescriptionSchema) -> SpamAssassinRuleDescription:
    res: SpamAssassinRuleDescription = db.exec(select(SpamAssassinRuleDescription).where(SpamAssassinRuleDescription.uuid == id)).first()
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


@router.patch('/{id}', summary='Partial update of a SpamAssassinRuleDescription', description='Updates the provided fields on a SpamAssassinRuleDescription')
async def partial_update(db: Annotated[Session, Depends(get_database_session)], id: uuid.UUID, data: SpamAssassinRuleDescriptionSchema) -> SpamAssassinRuleDescription:
    res: SpamAssassinRuleDescription = db.exec(select(SpamAssassinRuleDescription).where(SpamAssassinRuleDescription.uuid == id)).first()
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


@router.delete('/{id}', response_model=SpamAssassinRuleDescription, summary='Delete a SpamAssassinRuleDescription', description='Deletes a SpamAssassinRuleDescription from the system, after which we will no longer process data for it')
async def destroy(db: Annotated[Session, Depends(get_database_session)], id: uuid.UUID) -> None:
    res: SpamAssassinRuleDescription = db.exec(select(SpamAssassinRuleDescription).where(SpamAssassinRuleDescription.uuid == id)).first()
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    db.delete(res)
    db.commit()
