from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
import uuid
from typing import Any, List, Annotated
from mailguardian.app.http.pagination import paginate
from mailguardian.app.models.list_entry import ListEntry
from mailguardian.app.models.user import User
from mailguardian.app.schemas.audit_log import AuditAction
from mailguardian.app.schemas.list_entry import ListEntry as ListEntrySchema, ListingType
from sqlmodel import Session, select
from mailguardian.app.dependencies import get_database_session, oauth2_scheme, get_current_user, requires_app_admin
from mailguardian.app.schemas.pagination import PaginatedResponse
from mailguardian.app.schemas.user import UserRole
from mailguardian.app.utils.audit import audit_interaction

router = APIRouter(
    prefix='/blocklist',
    dependencies=[Depends(oauth2_scheme)],
    tags=['Blocklist']
)

# TODO: Find a way to more centrally define what is accessible
# For the initial implementation we will perform that logic in the routes directly,
# since the CLI tools are only used by admins

@router.get('', response_model=PaginatedResponse[ListEntry], summary='List all blocked senders', description='Returns a list of all blocked senders in the system')
async def index(db: Annotated[Session, Depends(get_database_session)], authenticated_user: Annotated[User, Depends(get_current_user)], q: str = Query(default=''), page: int = Query(1, ge=1), per_page: int = Query(20, ge=0)) -> PaginatedResponse[ListEntry]:
    # NOTE: By default the ListEntrys endpoint is not accessible to normal users, so we set the recordset to an empty list
    query = select(ListEntry).where(ListEntry.listing_type == ListingType.BLOCKED)
    # NOTE: A ListEntry Administrator can access the ListEntrys that they manage
    if authenticated_user.role == UserRole.DOMAIN_ADMINISTRATOR:
        query = select(ListEntry).where(
            ListEntry.listing_type == ListingType.BLOCKED and
            (ListEntry.from_domain in [domain.name for domain in authenticated_user.domains] or ListEntry.to_domain in [domain.name for domain in authenticated_user.domains])
        )
    elif authenticated_user.role == UserRole.USER:
        query = select(ListEntry).where((ListEntry.from_address == authenticated_user.email or ListEntry.to_address == authenticated_user.email) and ListEntry.listing_type == ListingType.BLOCKED)
    if q:
        query = query.where(ListEntry.from_address.contains(q) or ListEntry.to_address.contains(q))
    return await paginate(query=query, page=page, per_page=per_page)

@router.post('', response_model=ListEntry, summary='Create a new ListEntry', description='Creates a new ListEntry in the system')
async def store(db: Annotated[Session, Depends(get_database_session)], request: Request, authenticated_user: Annotated[User, Depends(get_current_user)], data: ListEntrySchema) -> ListEntry:
    # Ensure that if the domains were not provided, then we handle it here
    if not data.from_domain:
        local_part, domain_part = data.from_address.split('@')
        data.from_domain = domain_part
    if not data.to_domain:
        local_part, domain_part = data.to_address.split('@')
        data.to_domain = domain_part
    # TODO: Validate the in case of normal users or domain admins, we ensure that they are allowed to see this data
    # If a normal user, you need to be either the sender or the recipient to create the entry
    if authenticated_user.role == UserRole.USER:
        if authenticated_user.email not in [data.from_address, data.to_address]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='You cannot create a blocklist entry, which does not invovle your own email address'
            )
    # If you are a domain admin, you are allowed to create blocklist entries for emails/domains that you manage
    # This is evaluated by checking if the sending, or recieving, domain is part of the ones you manage
    if authenticated_user.role == UserRole.DOMAIN_ADMINISTRATOR:
        authenticated_domains: set[str] = set([domain.name for domain in authenticated_user.domains])
        if not data.from_domain in authenticated_domains and not data.to_domain in authenticated_domains:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='You cannot create a blocklist entry an email/domain that you do not manage'
            )
        
    # When all validation is done, we create the blocklist entry
    res: ListEntry = ListEntry(**data.model_dump())
    db.add(res)
    db.commit()
    audit_interaction(db=db, request=request, action=AuditAction.CREATE, model=ListEntry.__name__, res_id=res.id, actor_id=authenticated_user.id, message='Created Blocked Sender (%s)' % (res.id,))
    db.refresh(res)

    return res

@router.get('/{uuid}', response_model=ListEntry, summary='Output the details of a specific ListEntry', description='Using the UUID of a given ListEntry, the details of this is returned')
async def show(db: Annotated[Session, Depends(get_database_session)], authenticated_user: Annotated[User, Depends(get_current_user)], uuid: uuid.UUID) -> ListEntry:
    res: ListEntry = db.exec(select(ListEntry).where(ListEntry.uuid == uuid and ListEntry.listing_type == ListingType.BLOCKED)).first()
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    # If a normal user, you need to be either the sender or the recipient to create the entry
    if authenticated_user.role == UserRole.USER:
        if authenticated_user.email not in [res.from_address, res.to_address]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
            )
    # If you are a domain admin, you are allowed to create blocklist entries for emails/domains that you manage
    # This is evaluated by checking if the sending, or recieving, domain is part of the ones you manage
    if authenticated_user.role == UserRole.DOMAIN_ADMINISTRATOR:
        authenticated_domains: set[str] = set([domain.name for domain in authenticated_user.domains])
        if not res.from_domain in authenticated_domains and not res.to_domain in authenticated_domains:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
            )
    
    return res

@router.put('/{uuid}', response_model=ListEntry, summary='Update a ListEntry', description='Updates the full ListEntry record in the system')
async def update(db: Annotated[Session, Depends(get_database_session)], request: Request, authenticated_user: Annotated[User, Depends(get_current_user)], uuid: uuid.UUID, data: ListEntrySchema) -> ListEntry:
    res: ListEntry = db.exec(select(ListEntry).where(ListEntry.uuid == uuid and ListEntry.listing_type == ListingType.BLOCKED)).first()
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    # If a normal user, you need to be either the sender or the recipient to create the entry
    if authenticated_user.role == UserRole.USER:
        if authenticated_user.email not in [res.from_address, res.to_address]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
            )
    # If you are a domain admin, you are allowed to create blocklist entries for emails/domains that you manage
    # This is evaluated by checking if the sending, or recieving, domain is part of the ones you manage
    if authenticated_user.role == UserRole.DOMAIN_ADMINISTRATOR:
        authenticated_domains: set[str] = set([domain.name for domain in authenticated_user.domains])
        if not res.from_domain in authenticated_domains and not res.to_domain in authenticated_domains:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
            )
    
    res.sqlmodel_update(data.model_dump())
    db.add(res)
    db.commit()
    audit_interaction(db=db, request=request, action=AuditAction.UPDATE, model=ListEntry.__name__, res_id=res.id, actor_id=authenticated_user.id, message='Updated Blocked Sender (%s)' % (res.id,), old=res.model_dump(), new=data.model_dump())
    db.refresh(res)

    return res

@router.patch('/{uuid}', response_model=ListEntry, summary='Partial update of a ListEntry', description='Updates the provided fields on a ListEntry')
async def partial_update(db: Annotated[Session, Depends(get_database_session)], request: Request, authenticated_user: Annotated[User, Depends(get_current_user)], uuid: uuid.UUID, data: ListEntrySchema) -> ListEntry:
    res: ListEntry = db.exec(select(ListEntry).where(ListEntry.uuid == uuid and ListEntry.listing_type == ListingType.BLOCKED)).first()
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    # If a normal user, you need to be either the sender or the recipient to create the entry
    if authenticated_user.role == UserRole.USER:
        if authenticated_user.email not in [res.from_address, res.to_address]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
            )
    # If you are a domain admin, you are allowed to create blocklist entries for emails/domains that you manage
    # This is evaluated by checking if the sending, or recieving, domain is part of the ones you manage
    if authenticated_user.role == UserRole.DOMAIN_ADMINISTRATOR:
        authenticated_domains: set[str] = set([domain.name for domain in authenticated_user.domains])
        if not res.from_domain in authenticated_domains and not res.to_domain in authenticated_domains:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
            )
    data: dict[str, Any] = data.model_dump(exclude_unset=True)
    res.sqlmodel_update(data)
    db.add(res)
    db.commit()
    audit_interaction(db=db, request=request, action=AuditAction.UPDATE, model=ListEntry.__name__, res_id=res.id, actor_id=authenticated_user.id, message='Updated Blocked Sender (%s)' % (res.id,), old=res.model_dump(), new=data)
    db.refresh(res)

    return res

@router.delete('/{uuid}', response_model=ListEntry, summary='Delete a ListEntry', description='Deletes a ListEntry from the system, after which we will no longer process data for it')
async def destroy(db: Annotated[Session, Depends(get_database_session)], request: Request, authenticated_user: Annotated[User, Depends(get_current_user)], uuid: uuid.UUID) -> None:
    res: ListEntry = db.exec(select(ListEntry).where(ListEntry.uuid == uuid and ListEntry.listing_type == ListingType.BLOCKED)).first()
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    # If a normal user, you need to be either the sender or the recipient to create the entry
    if authenticated_user.role == UserRole.USER:
        if authenticated_user.email not in [res.from_address, res.to_address]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
            )
    # If you are a domain admin, you are allowed to create blocklist entries for emails/domains that you manage
    # This is evaluated by checking if the sending, or recieving, domain is part of the ones you manage
    if authenticated_user.role == UserRole.DOMAIN_ADMINISTRATOR:
        authenticated_domains: set[str] = set([domain.name for domain in authenticated_user.domains])
        if not res.from_domain in authenticated_domains and not res.to_domain in authenticated_domains:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
            )
    data: dict[str, Any] = res.model_dump()
    res_id: int = res.id
    db.delete(res)
    db.commit()
    audit_interaction(db=db, request=request, action=AuditAction.DELETE, model=ListEntry.__name__, res_id=res_id, actor_id=authenticated_user.id, message='Deleted Blocked Sender (%s)' % (res_id,), old=data, new={})