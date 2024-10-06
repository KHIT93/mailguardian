from mailguardian.config.app import settings
from typing import TYPE_CHECKING, Optional
from pathlib import Path
from pydantic import UUID4, EmailStr, IPvAnyAddress, AwareDatetime
from sqlmodel import Column, ForeignKey, Uuid, Integer, String, Boolean, Float, DateTime, Date, Field, SQLModel
import uuid

class SmtpRelay(SQLModel):

    ip_address: str = Field(max_length=255, index=True)
    hostname: str = Field(max_length=255, index=True, default='')
    active: bool = Field(default=False)
    comment: Optional[str] = Field(default=None)