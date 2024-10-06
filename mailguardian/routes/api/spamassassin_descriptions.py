from fastapi import APIRouter, Depends, HTTPException, status
import uuid
from typing import Any, List, Annotated
from mailguardian.app.models.spamassassin_rule_description import SpamAssassinRuleDescription
from mailguardian.app.models.user import User
from mailguardian.app.schemas.spamassassin_rule_description import SpamAssassinRuleDescription as SpamAssassinRuleDescriptionSchema
from sqlmodel import Session, select
from mailguardian.app.dependencies import get_database_session, oauth2_scheme, get_current_user, requires_app_admin

router = APIRouter(
    prefix='/spamassassin/descriptions',
    dependencies=[Depends(oauth2_scheme), Depends(requires_app_admin)],
    tags=['SpamAssassin Rules']
)

# TODO: Find a way to more centrally define what is accessible
# For the initial implementation we will perform that logic in the routes directly,
# since the CLI tools are only used by admins

@router.get('', response_model=List[SpamAssassinRuleDescription], summary='List all SpamAssassinRuleDescriptions', description='Returns a list of all SpamAssassinRuleDescriptions in the system')
async def index(db: Annotated[Session, Depends(get_database_session)], authenticated_user: Annotated[User, Depends(get_current_user)]) -> List[SpamAssassinRuleDescription]:
    results: List[SpamAssassinRuleDescription] = db.exec(select(SpamAssassinRuleDescription)).all()
    return results

@router.post('', response_model=SpamAssassinRuleDescription, summary='Create a new SpamAssassinRuleDescription', description='Creates a new SpamAssassinRuleDescription in the system')
async def store(db: Annotated[Session, Depends(get_database_session)], authenticated_user: Annotated[User, Depends(get_current_user)], data: SpamAssassinRuleDescriptionSchema) -> SpamAssassinRuleDescription:
    res: SpamAssassinRuleDescription = SpamAssassinRuleDescription(**data.model_dump())
    db.add(res)
    db.commit()
    db.refresh(res)

    return res

@router.get('/{uuid}', response_model=SpamAssassinRuleDescription, summary='Output the details of a specific SpamAssassinRuleDescription', description='Using the UUID of a given SpamAssassinRuleDescription, the details of this is returned')
async def show(db: Annotated[Session, Depends(get_database_session)], authenticated_user: Annotated[User, Depends(get_current_user)], uuid: uuid.UUID) -> SpamAssassinRuleDescription:
    res: SpamAssassinRuleDescription = db.exec(select(SpamAssassinRuleDescription).where(SpamAssassinRuleDescription.uuid == uuid)).first()
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    return res

@router.put('/{uuid}', response_model=SpamAssassinRuleDescription, summary='Update a SpamAssassinRuleDescription', description='Updates the full SpamAssassinRuleDescription record in the system')
async def update(db: Annotated[Session, Depends(get_database_session)], authenticated_user: Annotated[User, Depends(get_current_user)], uuid: uuid.UUID, data: SpamAssassinRuleDescriptionSchema) -> SpamAssassinRuleDescription:
    res: SpamAssassinRuleDescription = db.exec(select(SpamAssassinRuleDescription).where(SpamAssassinRuleDescription.uuid == uuid)).first()
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

@router.patch('/{uuid}', response_model=SpamAssassinRuleDescription, summary='Partial update of a SpamAssassinRuleDescription', description='Updates the provided fields on a SpamAssassinRuleDescription')
async def partial_update(db: Annotated[Session, Depends(get_database_session)], authenticated_user: Annotated[User, Depends(get_current_user)], uuid: uuid.UUID, data: SpamAssassinRuleDescriptionSchema) -> SpamAssassinRuleDescription:
    res: SpamAssassinRuleDescription = db.exec(select(SpamAssassinRuleDescription).where(SpamAssassinRuleDescription.uuid == uuid)).first()
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

@router.delete('/{uuid}', response_model=SpamAssassinRuleDescription, summary='Delete a SpamAssassinRuleDescription', description='Deletes a SpamAssassinRuleDescription from the system, after which we will no longer process data for it')
async def destroy(db: Annotated[Session, Depends(get_database_session)], authenticated_user: Annotated[User, Depends(get_current_user)], uuid: uuid.UUID) -> None:
    res: SpamAssassinRuleDescription = db.exec(select(SpamAssassinRuleDescription).where(SpamAssassinRuleDescription.uuid == uuid)).first()
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    db.delete(res)
    db.commit()