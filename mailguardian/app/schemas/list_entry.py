from mailguardian.config.app import settings
from enum import Enum
from typing import TYPE_CHECKING, Optional, Literal
from pathlib import Path
from pydantic import UUID4, EmailStr, IPvAnyAddress, AwareDatetime
from sqlmodel import Field, String, Column, SQLModel
import uuid

class ListingType(str, Enum):
    ALLOWED = 'allowed'
    BLOCKED = 'blocked'

class ListEntry(SQLModel):

    from_address: str = Field(nullable=False, index=True)
    from_domain : Optional[str] = Field(nullable=True, index=True)

    to_address: str = Field(nullable=False, index=True)
    to_domain : Optional[str] = Field(nullable=True, index=True)

    listing_type: ListingType = Field(index=True, max_length=12)