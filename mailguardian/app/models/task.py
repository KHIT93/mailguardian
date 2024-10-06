import enum
from mailguardian.app.models.base import BaseModel
from mailguardian.app.models.mailscanner_host import MailScannerHost
from mailguardian.config.app import settings
from typing import TYPE_CHECKING, Optional, Literal
from pathlib import Path
from pydantic import UUID4, EmailStr, IPvAnyAddress, AwareDatetime, Json
from ipaddress import IPv4Address, IPv6Address
from sqlmodel import Column, ForeignKey, Uuid, Integer, String, Boolean, Float, DateTime, Date, Field, JSON as SQLJson
import uuid
from uuid import UUID

class TaskState(enum.Enum):
    PENDING = 'PENDING'
    RECEIVED = 'RECEIVED'
    STARTED = 'STARTED'
    SUCCESS = 'SUCCESS'
    FAILURE = 'FAILURE'
    REVOKED = 'REVOKED'
    REJECTED = 'REJECTED'
    RETRY = 'RETRY'
    IGNORED = 'IGNORED'

class Task(BaseModel, table=True):
    __tablename__ = 'tasks'

    state: TaskState
    node_uuid: Optional[UUID] = Field(nullable=True, index=True, default='', description='The UUID of the designated to run this job')
    queue_uuid: Optional[UUID] = Field(nullable=True, index=True, default='', description='The UUID assigned by Celery. This will allow us to keep the state in sync between the two systems')
    module: str = Field(index=True, description='A full path to the python module to import for running this task')
    task: str = Field(index=True, description='THe name of method to execute on the module')
    payload: Optional[Json] = Field(nullable=True, default={}, description='A JSON-representation of the payload for the task to run', sa_type=SQLJson)
