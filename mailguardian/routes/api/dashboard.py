from fastapi import APIRouter, Depends, HTTPException, Query, status
import datetime
import uuid
from typing import Any, List, Annotated
from mailguardian.app.http.pagination import paginate
from mailguardian.app.models.audit_log import AuditLog
from mailguardian.app.models.message import Message
from mailguardian.app.models.user import User
from mailguardian.app.schemas.audit_log import AuditLog as AuditLogSchema
from sqlmodel import Session, select, func
from mailguardian.app.dependencies import get_database_session, oauth2_scheme, get_current_user, requires_app_admin
from mailguardian.app.schemas.dashboard import TrafficGraph, SenderCount
from mailguardian.app.schemas.pagination import PaginatedResponse
from mailguardian.app.schemas.user import UserRole

router = APIRouter(
    prefix='/dashboard',
    dependencies=[Depends(oauth2_scheme)],
    tags=['Dashboard']
)

@router.get('/traffic', response_model=List[TrafficGraph], summary='Dashboard Traffic statistics', description='Returns traffic statistics for the application dashboard')
async def traffic(db: Annotated[Session, Depends(get_database_session)], authenticated_user: Annotated[User, Depends(get_current_user)]) -> List[TrafficGraph]:
    end_date: datetime.date = datetime.date(year=2018, month=3, day=12)
    start_date: datetime.date = end_date - datetime.timedelta(days=30)
    query = select(Message).where(Message.from_address == authenticated_user.email or Message.to_address == authenticated_user.email)

    if authenticated_user.role == UserRole.SUPERUSER:
        query = select(Message)
    # NOTE: A Message Administrator can access the Messages that they manage
    elif authenticated_user.role == UserRole.DOMAIN_ADMINISTRATOR:
        query = select(Message).where(
            Message.from_domain in [domain.name for domain in authenticated_user.domains] or Message.to_domain in [domain.name for domain in authenticated_user.domains]
        )
    query = query.where(Message.date <= end_date).where(Message.date >= start_date).order_by(Message.date)

    # TODO: The next part performs like crap, since we generate the datastructure directly in Python instead of having the SQL database simply return a number for each date
    response_date: dict[datetime.date, int] = {}

    for record in db.exec(query).all():
        if record.date in response_date:
            response_date[record.date] += 1
        else:
            response_date[record.date] = 1

    

    single_dataset = [TrafficGraph(date=key, count=response_date[key]) for key in response_date.keys()]

    return single_dataset

@router.get('/senders', response_model=List[SenderCount], summary='Dashboard Traffic statistics', description='Returns traffic statistics for the application dashboard')
async def senders(db: Annotated[Session, Depends(get_database_session)], authenticated_user: Annotated[User, Depends(get_current_user)]) -> List[SenderCount]:
    end_date: datetime.date = datetime.date(year=2018, month=3, day=12)
    start_date: datetime.date = end_date - datetime.timedelta(days=30)
    query = select(Message).where(Message.from_address == authenticated_user.email or Message.to_address == authenticated_user.email)

    if authenticated_user.role == UserRole.SUPERUSER:
        query = select(Message)
    # NOTE: A Message Administrator can access the Messages that they manage
    elif authenticated_user.role == UserRole.DOMAIN_ADMINISTRATOR:
        query = select(Message).where(
            Message.from_domain in [domain.name for domain in authenticated_user.domains] or Message.to_domain in [domain.name for domain in authenticated_user.domains]
        )
    query = query.where(Message.date <= end_date).where(Message.date >= start_date).order_by(Message.date)

    sender_stats: dict[str, int] = {}
    # TODO: The next part performs like crap, since we generate the datastructure directly in Python instead of having the SQL database simply return a number for each date
    for record in db.exec(query).all():
        if not record.from_domain:
            continue
        if record.from_domain in sender_stats:
            sender_stats[record.from_domain] += 1
        else:
            sender_stats[record.from_domain] = 1
    
    sender_list: list[SenderCount] = [SenderCount(domain=sender, count=sender_stats[sender]) for sender in sender_stats.keys()]
    sender_list.sort(key=lambda x: x.count, reverse=True)

    return sender_list[:20]

@router.get('/spammers', response_model=List[SenderCount], summary='Dashboard Traffic statistics', description='Returns traffic statistics for the application dashboard')
async def spammers(db: Annotated[Session, Depends(get_database_session)], authenticated_user: Annotated[User, Depends(get_current_user)]) -> List[SenderCount]:
    end_date: datetime.date = datetime.date(year=2018, month=3, day=12)
    start_date: datetime.date = end_date - datetime.timedelta(days=30)
    query = select(Message).where(Message.from_address == authenticated_user.email or Message.to_address == authenticated_user.email)

    if authenticated_user.role == UserRole.SUPERUSER:
        query = select(Message)
    # NOTE: A Message Administrator can access the Messages that they manage
    elif authenticated_user.role == UserRole.DOMAIN_ADMINISTRATOR:
        query = select(Message).where(
            Message.from_domain in [domain.name for domain in authenticated_user.domains] or Message.to_domain in [domain.name for domain in authenticated_user.domains]
        )
    query = query.where(Message.date <= end_date).where(Message.date >= start_date).where(Message.is_spam).order_by(Message.date)

    spam_stats: dict[str, int] = {}
    # TODO: The next part performs like crap, since we generate the datastructure directly in Python instead of having the SQL database simply return a number for each date
    for record in db.exec(query).all():
        if not record.from_domain:
            continue
        if record.from_domain in spam_stats:
            spam_stats[record.from_domain] += 1
        else:
            spam_stats[record.from_domain] = 1
    
    sender_list: list[SenderCount] = [SenderCount(domain=sender, count=spam_stats[sender]) for sender in spam_stats.keys()]
    sender_list.sort(key=lambda x: x.count, reverse=True)

    return sender_list[:20]