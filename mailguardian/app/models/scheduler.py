import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

class KV(SQLModel, table=True):
    __tablename__ = 'scheduler_kv'

    queue: str = Field(primary_key=True)
    key: bytes = Field(primary_key=True)
    value: bytes

class Schedule(SQLModel, table=True):
    __tablename__ = 'scheduler_schedule'

    id: Optional[int] = Field(default=None, primary_key=True)
    queue: str
    data: bytes
    timestamp: datetime.datetime

class Task(SQLModel, table=True):
    __tablename__ = 'scheduler_tasks'

    id: Optional[int] = Field(default=None, primary_key=True)
    queue: str
    data: bytes
    priority: float = Field(default=0.0, index=True)