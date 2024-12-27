from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
import invoke
import uuid
from pymailq.store import PostqueueStore
from typing import Any, List, Annotated, Literal
from mailguardian.app.http.pagination import paginate
from mailguardian.app.models.audit_log import AuditLog
from mailguardian.app.models.message import Message
from mailguardian.app.models.message_transport_log import MessageTransportIdentifier, MessageTransportLog
from mailguardian.app.models.user import User
from mailguardian.app.schemas.audit_log import AuditAction
from mailguardian.app.schemas.message import Message as MessageSchema, MessageDetail, MessageProcessingQueue, ProcessableMessage
from mailguardian.app.schemas.message_header import MessageHeader as MessageHeaderSchema
from mailguardian.app.schemas.message_spam_report import MessageSpamReport as MessageSpamReportSchema
from mailguardian.app.schemas.message_mcp_report import MessageMcpReport as MessageMcpReportSchema
from mailguardian.app.schemas.message_rbl_report import MessageRblReport as MessageRblReportSchema
from mailguardian.app.schemas.message_transport_log import MessageTransportLog as MessageTransportLogSchema
from mailguardian.app.schemas.pagination import PaginatedResponse
from mailguardian.app.utils.audit import audit_interaction
from mailguardian.app.utils.messages import get_neutralized_message
from mailguardian.config.app import settings
from sqlmodel import Session, select
from mailguardian.app.dependencies import get_database_session, oauth2_scheme, get_current_user, requires_app_admin
from mailguardian.app.schemas.user import UserRole

router = APIRouter(
    prefix='/messages',
    dependencies=[Depends(oauth2_scheme)],
    tags=['Messages']
)

# TODO: Find a way to more centrally define what is accessible
# For the initial implementation we will perform that logic in the routes directly,
# since the CLI tools are only used by admins

@router.get('', response_model=PaginatedResponse[Message], summary='List all Messages', description='Returns a list of all Messages in the system')
async def index(db: Annotated[Session, Depends(get_database_session)], authenticated_user: Annotated[User, Depends(get_current_user)], page: int = Query(1, ge=1), per_page: int = Query(20, ge=0)) -> PaginatedResponse[Message]:
    # NOTE: By default the Messages endpoint is not accessible to normal users, so we set the recordset to an empty list
    # results: List[Message] = []
    # NOTE: An Application Administrator can access everything
    query = select(Message).where(Message.from_address == authenticated_user.email or Message.to_address == authenticated_user.email)

    if authenticated_user.role == UserRole.SUPERUSER:
        query = select(Message)
    # NOTE: A Message Administrator can access the Messages that they manage
    elif authenticated_user.role == UserRole.DOMAIN_ADMINISTRATOR:
        query = select(Message).where(
            Message.from_domain in [domain.name for domain in authenticated_user.domains] or Message.to_domain in [domain.name for domain in authenticated_user.domains]
        )
    query = query.order_by(Message.date)
    # return results
    return await paginate(query=query, page=page, per_page=per_page)

@router.get('/{uuid}', response_model=Message, summary='Output the details of a specific Message', description='Using the UUID of a given Message, the details of this is returned')
async def show(db: Annotated[Session, Depends(get_database_session)], request: Request, authenticated_user: Annotated[User, Depends(get_current_user)], uuid: uuid.UUID) -> Message:
    res: Message = db.exec(select(Message).where(Message.uuid == uuid and Message.listing_type == 'blocked')).first()
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
    
    audit_interaction(db=db, request=request, action=AuditAction.READ, model=Message.__name__, res_id=res.id, actor_id=authenticated_user.id, message='Viewed Message (%s)' % (res.mailq_id,))
    
    db.refresh(res)
    return res

@router.get('/{uuid}/headers', response_model=List[MessageHeaderSchema], summary='Output the headers of a specific Message', description='Using the UUID of a given Message, the headers of this is returned')
async def show_headers(db: Annotated[Session, Depends(get_database_session)], authenticated_user: Annotated[User, Depends(get_current_user)], uuid: uuid.UUID) -> List[MessageHeaderSchema]:
    res: Message = db.exec(select(Message).where(Message.uuid == uuid and Message.listing_type == 'blocked')).first()
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
    return res.headers

@router.get('/{uuid}/reports/spam', response_model=List[MessageSpamReportSchema], summary='Output the spam report of a specific Message', description='Using the UUID of a given Message, the spam report of this is returned')
async def show_headers(db: Annotated[Session, Depends(get_database_session)], authenticated_user: Annotated[User, Depends(get_current_user)], uuid: uuid.UUID) -> List[MessageSpamReportSchema]:
    res: Message = db.exec(select(Message).where(Message.uuid == uuid and Message.listing_type == 'blocked')).first()
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
    
    return res.spam_reports

@router.get('/{uuid}/reports/mcp', response_model=List[MessageMcpReportSchema], summary='Output the MCP report of a specific Message', description='Using the UUID of a given Message, the MCP report of this is returned')
async def show_headers(db: Annotated[Session, Depends(get_database_session)], authenticated_user: Annotated[User, Depends(get_current_user)], uuid: uuid.UUID) -> List[MessageMcpReportSchema]:
    res: Message = db.exec(select(Message).where(Message.uuid == uuid and Message.listing_type == 'blocked')).first()
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
    
    return res.mcp_reports

@router.get('/{uuid}/reports/rbl', response_model=List[MessageRblReportSchema], summary='Output the RBL report of a specific Message', description='Using the UUID of a given Message, the RBL report of this is returned')
async def show_headers(db: Annotated[Session, Depends(get_database_session)], authenticated_user: Annotated[User, Depends(get_current_user)], uuid: uuid.UUID) -> List[MessageRblReportSchema]:
    res: Message = db.exec(select(Message).where(Message.uuid == uuid and Message.listing_type == 'blocked')).first()
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
    
    return res.rbl_reports

@router.get('/{uuid}/logs', response_model=List[MessageTransportLogSchema], summary='Output the Transport logs of a specific Message', description='Using the UUID of a given Message, the Transport logs of this is returned')
async def show_transport_log(db: Annotated[Session, Depends(get_database_session)], authenticated_user: Annotated[User, Depends(get_current_user)], uuid: uuid.UUID) -> List[MessageTransportLogSchema]:
    res: Message = db.exec(select(Message).where(Message.uuid == uuid and Message.listing_type == 'blocked')).first()
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
    
    # TODO: Figure out how to use MessageTransportIdentifier to find entries that might not be directly linked to the record it self
    mta_log_ids: List[MessageTransportIdentifier] = db.exec(select(MessageTransportIdentifier).where(MessageTransportIdentifier.smtpd_id == res.mailq_id))

    extra_transport_logs: List[MessageTransportLog] = db.exec(select(MessageTransportLog).where(MessageTransportLog.mail_message_id in [ml.smtp_id for ml in mta_log_ids])).all() if mta_log_ids else []
    
    return res.transport_logs + extra_transport_logs

@router.get('/{uuid}/view', response_model=List[MessageDetail], summary='Output the Transport logs of a specific Message', description='Using the UUID of a given Message, the Transport logs of this is returned')
async def view_message_contents(db: Annotated[Session, Depends(get_database_session)], request: Request, authenticated_user: Annotated[User, Depends(get_current_user)], uuid: uuid.UUID) -> List[MessageDetail]:
    res: Message = db.exec(select(Message).where(Message.uuid == uuid and Message.listing_type == 'blocked')).first()
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
    
    # Find the message in the filesystem and process it
    if not res.queue_file_exists():
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail='No message found to display'
        )
    
    message_details: MessageDetail = get_neutralized_message(message=res.file_path())

    audit_interaction(db=db, request=request, action=AuditAction.READ, model=Message.__name__, res_id=res.id, actor_id=authenticated_user.id, message='Viewed Message Contents (%s)' % (res.mailq_id,))
    
    return message_details

@router.post('/{uuid}/learn', response_model=bool, summary='Teach the system how to look at this type of message in the future', description='Using this endpoint you will be able to teach SpamAssassin if this message is spam or not spam')
async def spamassassin_learn(db: Annotated[Session, Depends(get_database_session)], request: Request, authenticated_user: Annotated[User, Depends(get_current_user)], uuid: uuid.UUID, type: Literal['spam', 'ham']) -> bool:
    res: Message = db.exec(select(Message).where(Message.uuid == uuid and Message.listing_type == 'blocked')).first()
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
    
    # TODO: Make this work with multi-node once we have a solution for it, since the file exists on each node and not on necessarily on the node running the API
    
    if not res.queue_file_exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='The specified message could not be found in the storage'
        )
        
    if type == 'spam':
        type = '-r'
    if type == 'ham':
        type = '-k'

    invoke.run(f'spamassassin -p {settings.SA_PREF} {type} < {res.file_path()} 2>&1')

    audit_interaction(db=db, request=request, action=AuditAction.UPDATE, model=Message.__name__, res_id=res.id, actor_id=authenticated_user.id, message='Learned Message (%s) as %s' % (res.mailq_id, type))

    return True

@router.delete('/queue', response_model=MessageProcessingQueue, summary='View the mail processing queue', description='Returns the list of items on the email processing queue of the MTA', dependencies=[Depends(requires_app_admin)])
async def view_mailqueue(db: Annotated[Session, Depends(get_database_session)], request: Request, authenticated_user: Annotated[User, Depends(get_current_user)]) -> MessageProcessingQueue:
    store: PostqueueStore = PostqueueStore()
    store.load()
    res: MessageProcessingQueue = MessageProcessingQueue(messages=[
        ProcessableMessage(**mail) for mail in store.mails
    ])

    audit_interaction(db=db, request=request, action=AuditAction.READ, model=Message.__name__, res_id=None, actor_id=authenticated_user.id, message='Viewed Mail Processing Queue')

    return res