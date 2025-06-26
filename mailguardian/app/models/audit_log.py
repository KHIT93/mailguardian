from mailguardian.app.models.base import BaseModel
from mailguardian.app.schemas.audit_log import AuditLog as AuditLogSchema


class AuditLog(AuditLogSchema, BaseModel, table=True):
    __tablename__ = 'audit_log'
