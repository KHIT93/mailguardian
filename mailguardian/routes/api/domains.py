import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlmodel import Session, select

from mailguardian.app.dependencies import (
    get_current_user,
    get_database_session,
    oauth2_scheme,
    requires_app_admin,
)
from mailguardian.app.http.pagination import paginate
from mailguardian.app.models.domain import Domain as Domain
from mailguardian.app.models.user import User
from mailguardian.app.schemas.audit_log import AuditAction
from mailguardian.app.schemas.domain import Domain as DomainSchema
from mailguardian.app.schemas.pagination import PaginatedResponse
from mailguardian.app.schemas.user import UserRole
from mailguardian.app.utils.audit import audit_interaction

router = APIRouter(
    prefix='/domains',
    dependencies=[Depends(oauth2_scheme)],
    tags=['Domains']
)

# TODO: Find a way to more centrally define what is accessible
# For the initial implementation we will perform that logic in the routes directly,
# since the CLI tools are only used by admins


@router.get('', summary='List all domains', description='Returns a list of all domains in the system')
async def index(db: Annotated[Session, Depends(get_database_session)], authenticated_user: Annotated[User, Depends(get_current_user)], q: Annotated[str, Query()] = '', page: Annotated[int, Query(ge=1)] = 1, per_page: Annotated[int, Query(ge=0)] = 20) -> PaginatedResponse[Domain]:
    # NOTE: By default the domains endpoint is not accessible to normal users, so we set the recordset to an empty list
    # NOTE: A Domain Administrator can access the domains that they manage
    current_user = db.exec(select(User).where(User.id == authenticated_user.id)).first()
    query = select(Domain).where(Domain.id in current_user.domains)
    # NOTE: An Application Administrator can access everything
    if authenticated_user.role == UserRole.SUPERUSER:
        query = select(Domain)
    else:
        if authenticated_user.role not in [UserRole.DOMAIN_ADMINISTRATOR, UserRole.SUPERUSER]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='You do not have access'
            )
    if q:
        query = query.where(Domain.name.contains(q))
    return await paginate(query=query, page=page, per_page=per_page)


@router.post('', summary='Create a new domain', description='Creates a new domain in the system', dependencies=[Depends(requires_app_admin)])
async def store(db: Annotated[Session, Depends(get_database_session)], request: Request, authenticated_user: Annotated[User, Depends(get_current_user)], data: DomainSchema) -> Domain:
    res: Domain = Domain(**data.model_dump())
    db.add(res)
    db.commit()
    audit_interaction(db=db, request=request, action=AuditAction.CREATE, model=Domain.__name__, res_id=res.id, actor_id=authenticated_user.id, message=f'Created Domain ({res.name})')
    db.refresh(res)

    return res


@router.get('/{id}', summary='Output the details of a specific domain', description='Using the UUID of a given domain, the details of this is returned')
async def show(db: Annotated[Session, Depends(get_database_session)], authenticated_user: Annotated[User, Depends(get_current_user)], id: uuid.UUID) -> Domain:
    if not authenticated_user.role == UserRole.SUPERUSER and not authenticated_user.is_domain_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You do not have access'
        )
    res: Domain = db.exec(select(Domain).where(Domain.uuid == id)).first()
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    if authenticated_user.is_domain_admin:
        if res not in authenticated_user.domains:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND
            )
    return res


@router.put('/{id}', summary='Update a domain', description='Updates the full domain record in the system')
async def update(db: Annotated[Session, Depends(get_database_session)], request: Request, authenticated_user: Annotated[User, Depends(get_current_user)], id: uuid.UUID, domain: DomainSchema) -> Domain:
    res: Domain = db.exec(select(Domain).where(Domain.uuid == id)).first()
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    domain_data: dict[str, Any] = domain.model_dump()
    res.sqlmodel_update(domain_data)
    db.add(res)
    db.commit()
    audit_interaction(db=db, request=request, action=AuditAction.UPDATE, model=Domain.__name__, res_id=res.id, actor_id=authenticated_user.id, message=f'Updated Domain ({res.name})', old=res.model_dump(), new=domain.model_dump())
    db.refresh(res)

    return res


@router.patch('/{id}', summary='Partial update of a domain', description='Updates the provided fields on a domain')
async def partial_update(db: Annotated[Session, Depends(get_database_session)], request: Request, authenticated_user: Annotated[User, Depends(get_current_user)], id: uuid.UUID, domain: DomainSchema) -> Domain:
    res: Domain = db.exec(select(Domain).where(Domain.uuid == id)).first()
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    domain_data: dict[str, Any] = domain.model_dump(exclude_unset=True)
    res.sqlmodel_update(domain_data)
    db.add(res)
    db.commit()
    audit_interaction(db=db, request=request, action=AuditAction.UPDATE, model=Domain.__name__, res_id=res.id, actor_id=authenticated_user.id, message=f'Updated Domain ({res.name})', old=res.model_dump(), new=domain.model_dump())
    db.refresh(res)

    return res


@router.delete('/{id}', response_model=Domain, summary='Delete a domain', description='Deletes a domain from the system, after which we will no longer process data for it', dependencies=[Depends(requires_app_admin)])
async def destroy(db: Annotated[Session, Depends(get_database_session)], request: Request, authenticated_user: Annotated[User, Depends(get_current_user)], id: uuid.UUID) -> None:
    res: Domain = db.exec(select(Domain).where(Domain.uuid == id)).first()
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    res_id: int = res.id
    res_name: str = res.name
    data: dict[str, Any] = res.model_dump()
    db.delete(res)
    db.commit()
    audit_interaction(db=db, request=request, action=AuditAction.DELETE, model=Domain.__name__, res_id=res_id, actor_id=authenticated_user.id, message=f'Deleted Domain ({res_name})', old=data, new={})
