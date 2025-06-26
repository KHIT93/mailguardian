import enum
from uuid import UUID

from pydantic import Json
from sqlmodel import JSON as SQLJson
from sqlmodel import Field

from mailguardian.app.models.base import BaseModel


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
    node_uuid: UUID | None = Field(nullable=True, index=True, default='', description='The UUID of the designated to run this job')
    queue_uuid: UUID | None = Field(nullable=True, index=True, default='', description='The UUID assigned by Celery. This will allow us to keep the state in sync between the two systems')
    module: str = Field(index=True, description='A full path to the python module to import for running this task')
    task: str = Field(index=True, description='THe name of method to execute on the module')
    payload: Json | None = Field(nullable=True, default={}, description='A JSON-representation of the payload for the task to run', sa_type=SQLJson)
