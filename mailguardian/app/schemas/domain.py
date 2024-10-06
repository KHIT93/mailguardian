from datetime import datetime, timezone
from enum import Enum
from pydantic import UUID4, EmailStr, AwareDatetime
from typing import TYPE_CHECKING, List, Optional, Literal
from sqlmodel import Field, Relationship, DateTime, SQLModel

import uuid

class ReceptionType(Enum):
    LOAD_BALANCED = 'load_balanced'
    FAILOVER = 'failover'

class Domain(SQLModel):

    name: str = Field(index=True, unique=True, max_length=128)
    destination: Optional[str] = Field(default=None, max_length=128, nullable=True)
    relay_type: str = Field(default='smtp', max_length=64)

    # TODO: Find out how to set this server side
    created_at: datetime = Field(default=datetime.now(timezone.utc))
    # TODO: Find out how to force an updated value of this on save
    updated_at: datetime
    
    active: bool = Field(default=False)
    catchall: bool = Field(default=False)

    # was receive_type
    reception_type: ReceptionType = Field(default=ReceptionType.FAILOVER)

    def __str__(self):
        return self.name