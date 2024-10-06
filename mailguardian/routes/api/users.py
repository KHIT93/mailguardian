from fastapi import APIRouter, Depends, HTTPException, Query, status
import uuid
from typing import Any, List, Annotated
from mailguardian.app.http.pagination import paginate
from mailguardian.app.auth.utils import hash_password, validate_new_password
from mailguardian.app.models.user import User
from mailguardian.app.models.domain import Domain
from mailguardian.app.schemas.user import User as UserSchema, UserCreation
from mailguardian.app.schemas.pagination import PaginatedResponse
from sqlmodel import Session, select
from mailguardian.app.dependencies import get_database_session, oauth2_scheme, get_current_user, requires_app_admin

router = APIRouter(
    prefix='/users',
    dependencies=[Depends(oauth2_scheme), Depends(requires_app_admin)],
    tags=['Users']
)

# TODO: Find a way to more centrally define what is accessible
# For the initial implementation we will perform that logic in the routes directly,
# since the CLI tools are only used by admins

@router.get('', response_model=PaginatedResponse[User], summary='List all users', description='Returns a list of all users in the system')
async def index(db: Annotated[Session, Depends(get_database_session)], authenticated_user: Annotated[User, Depends(get_current_user)], q: str = Query(default=''), page: int = Query(1, ge=1), per_page: int = Query(20, ge=0)) -> PaginatedResponse[User]:
    query = select(User)
    if q:
        query = query.where(User.email.contains(q))
    return await paginate(query=query, page=page, per_page=per_page)

@router.post('', response_model=User, summary='Create a new user', description='Creates a new user in the system')
async def store(db: Annotated[Session, Depends(get_database_session)], authenticated_user: Annotated[User, Depends(get_current_user)], user: UserCreation) -> User:
    validate_new_password(plain_password=user.passwd)
    res: User = User.model_validate(user, update={'password': hash_password(password=user.passwd)})
    db.add(res)
    db.commit()
    db.refresh(res)

    return res

@router.get('/{uuid}', response_model=User, summary='Output the details of a specific user', description='Using the UUID of a given user, the details of this is returned')
async def show(db: Annotated[Session, Depends(get_database_session)], authenticated_user: Annotated[User, Depends(get_current_user)], uuid: uuid.UUID) -> User:
    res: User = db.exec(select(User).where(User.uuid == uuid)).first()
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    return res

@router.put('/{uuid}', response_model=User, summary='Update a user', description='Updates the full user record in the system')
async def update(db: Annotated[Session, Depends(get_database_session)], authenticated_user: Annotated[User, Depends(get_current_user)], uuid: uuid.UUID, user: UserSchema) -> User:
    res: User = db.exec(select(User).where(User.uuid == uuid)).first()
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    user_data: dict[str, Any] = user.model_dump()
    res.sqlmodel_update(user_data)
    db.add(res)
    db.commit()
    db.refresh(res)

    return res

@router.patch('/{uuid}', response_model=User, summary='Partial update of a user', description='Updates the provided fields on a user')
async def partial_update(db: Annotated[Session, Depends(get_database_session)], authenticated_user: Annotated[User, Depends(get_current_user)], uuid: uuid.UUID, user: UserSchema) -> User:
    res: User = db.exec(select(User).where(User.uuid == uuid)).first()
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    user_data: dict[str, Any] = user.model_dump(exclude_unset=True)
    res.sqlmodel_update(user_data)
    db.add(res)
    db.commit()
    db.refresh(res)

    return res

@router.delete('/{uuid}', response_model=User, summary='Delete a user', description='Deletes a user from the system, after which we will no longer process data for it')
async def destroy(db: Annotated[Session, Depends(get_database_session)], authenticated_user: Annotated[User, Depends(get_current_user)], uuid: uuid.UUID) -> None:
    res: User = db.exec(select(User).where(User.uuid == uuid)).first()
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    db.delete(res)
    db.commit()




@router.get('/{uuid}/domains', response_model=List[Domain], summary='List the users domains', description='Lists the domains that this user can manage')
async def show_domains(db: Annotated[Session, Depends(get_database_session)], authenticated_user: Annotated[User, Depends(get_current_user)], uuid: uuid.UUID) -> List[Domain]:
    res: User = db.exec(select(User).where(User.uuid == uuid)).first()
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    return res.domains

@router.post('/{uuid}/domains/{domain_uuid}', response_model=User, summary='Add a domain to a user', description='Adds the link between the user and the domain, which results in the user being able to manage it')
async def destroy(db: Annotated[Session, Depends(get_database_session)], authenticated_user: Annotated[User, Depends(get_current_user)], uuid: uuid.UUID, domain_uuid: uuid.UUID) -> List[Domain]:
    res: User = db.exec(select(User).where(User.uuid == uuid)).first()
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    domain: Domain = db.exec(select(Domain).where(Domain.uuid == domain_uuid)).first()
    if not domain:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    res.domains.append(domain)
    db.add(res)
    db.commit()
    db.refresh(res)
    return res.domains

@router.delete('/{uuid}/domains/{domain_uuid}', response_model=User, summary='Delete a domain from a user', description='Deletes the link between the user and the domain, which results in the user no longer being able to manage it')
async def destroy(db: Annotated[Session, Depends(get_database_session)], authenticated_user: Annotated[User, Depends(get_current_user)], uuid: uuid.UUID, domain_uuid: uuid.UUID) -> None:
    res: User = db.exec(select(User).where(User.uuid == uuid)).first()
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    domain: Domain = db.exec(select(Domain).where(Domain.uuid == domain_uuid)).first()
    if not domain:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    res.domains.remove(domain)
    db.add(res)
    db.commit()