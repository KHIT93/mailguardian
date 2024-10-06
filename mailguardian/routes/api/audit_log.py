from fastapi import APIRouter, Depends, HTTPException, Query, status
import uuid
from typing import Any, List, Annotated
from mailguardian.app.http.pagination import paginate
from mailguardian.app.models.audit_log import AuditLog
from mailguardian.app.models.user import User
from mailguardian.app.schemas.audit_log import AuditLog as AuditLogSchema
from sqlmodel import Session, select
from mailguardian.app.dependencies import get_database_session, oauth2_scheme, get_current_user, requires_app_admin
from mailguardian.app.schemas.pagination import PaginatedResponse

router = APIRouter(
    prefix='/audit/log',
    dependencies=[Depends(oauth2_scheme), Depends(requires_app_admin)],
    tags=['Audit Logging']
)

# TODO: Find a way to more centrally define what is accessible
# For the initial implementation we will perform that logic in the routes directly,
# since the CLI tools are only used by admins

@router.get('', response_model=PaginatedResponse[AuditLog], summary='List all AuditLogs', description='Returns a list of all AuditLogs in the system')
async def index(db: Annotated[Session, Depends(get_database_session)], authenticated_user: Annotated[User, Depends(get_current_user)], page: int = Query(1, ge=1), per_page: int = Query(20, ge=0)) -> PaginatedResponse[AuditLog]:
    # NOTE: By default the AuditLogs endpoint is not accessible to normal users, so we set the recordset to an empty list
    query = select(AuditLog)
    return await paginate(query=query, page=page, per_page=per_page)

@router.get('/{uuid}', response_model=AuditLog, summary='Output the details of a specific AuditLog', description='Using the UUID of a given AuditLog, the details of this is returned')
async def show(db: Annotated[Session, Depends(get_database_session)], authenticated_user: Annotated[User, Depends(get_current_user)], uuid: uuid.UUID) -> AuditLog:
    res: AuditLog = db.exec(select(AuditLog).where(AuditLog.uuid == uuid and AuditLog.listing_type == 'blocked')).first()
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    return res