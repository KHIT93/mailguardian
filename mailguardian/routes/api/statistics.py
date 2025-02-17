import datetime
from typing import Annotated
from fastapi import APIRouter, Depends, Request
from sqlmodel import Session, select

from mailguardian.app.dependencies import (
    get_current_user,
    get_database_session,
    oauth2_scheme,
    requires_app_admin,
)
from mailguardian.app.models.user import User
from mailguardian.app.models.message import Message
from mailguardian.app.schemas.statistics import MessageFilter, StatisticsResponse, MessageStatistics, FilterOperator
from mailguardian.app.schemas.user import UserRole

router = APIRouter(
    prefix='/statistics',
    dependencies=[Depends(oauth2_scheme)],
    tags=['Statistics']
)

@router.post('/messages', summary='Statistics Endpoint for email messages', description='A generic endpoint for handling statistic queries into message data')
def message_stats(db: Annotated[Session, Depends(get_database_session)], request: Request, authenticated_user: Annotated[User, Depends(get_current_user)], filters: list[MessageFilter]) -> MessageStatistics:
    filter_fields: list[str] = [filter.field for filter in filters]
    print(filters)
    
    query = select(Message)
    
    apply_from_address_filter: bool = True
    apply_to_address_filter: bool = True
    apply_from_domain_filter: bool = True
    apply_to_domain_filter: bool = True

    if authenticated_user.role == UserRole.DOMAIN_ADMINISTRATOR:
        apply_from_address_filter = False
        apply_to_address_filter = False
    
    elif authenticated_user.role == UserRole.SUPERUSER:
        apply_from_address_filter = False
        apply_from_domain_filter = False
        apply_to_address_filter = False
        apply_to_domain_filter = False
    
    for filter in filters:
        if filter.field == 'date':
            filter.value = datetime.datetime.strptime(filter.value, '%Y-%m-%d').date()
        
        if filter.operator == FilterOperator.EQUAL:
            query = query.where(getattr(Message, filter.field) == filter.value)
        elif filter.operator == FilterOperator.NOT_EQUAL:
            query = query.where(getattr(Message, filter.field) != filter.value)
        elif filter.operator == FilterOperator.GREATER_THAN:
            query = query.where(getattr(Message, filter.field) > filter.value)
        elif filter.operator == FilterOperator.LESS_THAN:
            query = query.where(getattr(Message, filter.field) < filter.value)

    if apply_from_address_filter and apply_to_address_filter:
        query = query.where(Message.from_address == authenticated_user.email or Message.to_address == authenticated_user.email)
    elif apply_from_address_filter:
        query = query.where(Message.from_address == authenticated_user.email)
    elif apply_to_address_filter:
        query = query.where(Message.to_address == authenticated_user.email)
    elif apply_from_domain_filter and apply_to_domain_filter:
        query = query.where(Message.from_domain in [domain.name for domain in authenticated_user.domains] or Message.to_domain in [domain.name for domain in authenticated_user.domains])
    elif apply_from_domain_filter:
        query = query.where(Message.from_domain in [domain.name for domain in authenticated_user.domains])
    elif apply_to_domain_filter:
        query = query.where(Message.to_domain in [domain.name for domain in authenticated_user.domains])

    result: list[Message] = db.exec(query.order_by(Message.timestamp)).all()
    if result:
        return MessageStatistics(total=len(result), first_date=result[0].date, last_date=result[-1].date, items=result)
    else:
        return MessageStatistics(total=0, first_date=None, last_date=None, items=[])