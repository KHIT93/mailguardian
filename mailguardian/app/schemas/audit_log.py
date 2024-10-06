from datetime import datetime, timezone
from enum import Enum
from ipaddress import IPv4Address, IPv6Address
from typing import TYPE_CHECKING, List, Optional
from sqlmodel import Column, ForeignKey, Uuid, Integer, String, Boolean, Field, Relationship, SQLModel
import uuid

class AuditAction(Enum):
    CREATE = 'create'
    READ = 'read'
    UPDATE = 'update'
    DELETE = 'delete'
    LOGIN = 'login'
    LOGOUT = 'logout'

class AuditLog(SQLModel):
    model: str = Field(description='The database model on which the action was performed')
    res_id: Optional[int] = Field(description='The ID of the record in the database model, on which the action was performed')

    action: AuditAction

    actor_id: Optional[int] = Field(foreign_key="users.id", description='The ID of the user who performed the action')
    acted_from: str = Field(description='The IPv4/IPv6 address from which the action was performed')
    performed_at: datetime = Field(default=datetime.now(timezone.utc))

    # TODO: Evaluate if this should be a relationship in the end
    # TODO: Find out how to certain non-CRUD actions, such as when logging in or releasing messages from quarantine
    changes: Optional[str] = Field(description='JSON object with the values that changed')

    message: Optional[str] = Field(description='A message connected to the auditted action')

    allowed: bool = Field(description='Indicates whether the logged interaction was allowed or denied', default=True)