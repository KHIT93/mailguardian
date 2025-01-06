import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from mailguardian.app.dependencies import (
    get_database_session,
    oauth2_scheme,
    requires_app_admin,
)
from mailguardian.app.models.spamassassin_rule import SpamAssassinRule
from mailguardian.app.schemas.spamassassin_rule import (
    SpamAssassinRule as SpamAssassinRuleSchema,
)

router = APIRouter(
    prefix='/spamassassin/rules',
    dependencies=[Depends(oauth2_scheme), Depends(requires_app_admin)],
    tags=['SpamAssassin Rules']
)

# TODO: Find a way to more centrally define what is accessible
# For the initial implementation we will perform that logic in the routes directly,
# since the CLI tools are only used by admins


@router.get('', summary='List all SpamAssassinRules', description='Returns a list of all SpamAssassinRules in the system')
async def index(db: Annotated[Session, Depends(get_database_session)]) -> list[SpamAssassinRule]:
    results: list[SpamAssassinRule] = db.exec(select(SpamAssassinRule)).all()
    return results


@router.post('', summary='Create a new SpamAssassinRule', description='Creates a new SpamAssassinRule in the system')
async def store(db: Annotated[Session, Depends(get_database_session)], data: SpamAssassinRuleSchema) -> SpamAssassinRule:
    res: SpamAssassinRule = SpamAssassinRule(**data.model_dump())
    db.add(res)
    db.commit()
    db.refresh(res)

    return res


@router.get('/{id}', summary='Output the details of a specific SpamAssassinRule', description='Using the UUID of a given SpamAssassinRule, the details of this is returned')
async def show(db: Annotated[Session, Depends(get_database_session)], id: uuid.UUID) -> SpamAssassinRule:
    res: SpamAssassinRule = db.exec(select(SpamAssassinRule).where(SpamAssassinRule.uuid == id)).first()
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    return res


@router.put('/{id}', summary='Update a SpamAssassinRule', description='Updates the full SpamAssassinRule record in the system')
async def update(db: Annotated[Session, Depends(get_database_session)], id: uuid.UUID, data: SpamAssassinRuleSchema) -> SpamAssassinRule:
    res: SpamAssassinRule = db.exec(select(SpamAssassinRule).where(SpamAssassinRule.uuid == id)).first()
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


@router.patch('/{id}', summary='Partial update of a SpamAssassinRule', description='Updates the provided fields on a SpamAssassinRule')
async def partial_update(db: Annotated[Session, Depends(get_database_session)], id: uuid.UUID, data: SpamAssassinRuleSchema) -> SpamAssassinRule:
    res: SpamAssassinRule = db.exec(select(SpamAssassinRule).where(SpamAssassinRule.uuid == id)).first()
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


@router.delete('/{id}', response_model=SpamAssassinRule, summary='Delete a SpamAssassinRule', description='Deletes a SpamAssassinRule from the system, after which we will no longer process data for it')
async def destroy(db: Annotated[Session, Depends(get_database_session)], id: uuid.UUID) -> None:
    res: SpamAssassinRule = db.exec(select(SpamAssassinRule).where(SpamAssassinRule.uuid == id)).first()
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    db.delete(res)
    db.commit()
