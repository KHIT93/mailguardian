import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select

from mailguardian.app.dependencies import (
    get_database_session,
    oauth2_scheme,
    requires_app_admin,
)
from mailguardian.app.http.pagination import paginate
from mailguardian.app.models.audit_log import AuditLog
from mailguardian.app.schemas.pagination import PaginatedResponse

router = APIRouter(
    prefix='/audit/log',
    dependencies=[Depends(oauth2_scheme), Depends(requires_app_admin)],
    tags=['Audit Logging']
)

# TODO: Find a way to more centrally define what is accessible
# For the initial implementation we will perform that logic in the routes directly,
# since the CLI tools are only used by admins


@router.get('', summary='List all AuditLogs', description='Returns a list of all AuditLogs in the system')
async def index(page: Annotated[int, Query(1, ge=1)], per_page: Annotated[int, Query(20, ge=0)]) -> PaginatedResponse[AuditLog]:
    # NOTE: By default the AuditLogs endpoint is not accessible to normal users, so we set the recordset to an empty list
    query = select(AuditLog)
    return await paginate(query=query, page=page, per_page=per_page)


@router.get('/{id}', summary='Output the details of a specific AuditLog', description='Using the UUID of a given AuditLog, the details of this is returned')
async def show(db: Annotated[Session, Depends(get_database_session)], id: uuid.UUID) -> AuditLog:
    res: AuditLog = db.exec(select(AuditLog).where(AuditLog.uuid == id and AuditLog.listing_type == 'blocked')).first()
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )

    return res
