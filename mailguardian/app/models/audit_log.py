from mailguardian.app.models.base import BaseModel
from mailguardian.app.schemas.audit_log import AuditLog as AuditLogSchema
from datetime import datetime
from pydantic import UUID4, EmailStr, AwareDatetime
from typing import TYPE_CHECKING, List, Optional, Literal
from sqlmodel import Field, Relationship, DateTime


class AuditLog(AuditLogSchema, BaseModel, table=True):
    __tablename__ = 'audit_log'