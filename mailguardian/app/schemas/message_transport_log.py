import datetime
from mailguardian.config.app import settings
from typing import TYPE_CHECKING, Optional
from pathlib import Path
from pydantic import UUID4, EmailStr, IPvAnyAddress, AwareDatetime
from sqlmodel import Column, ForeignKey, Uuid, Integer, String, Boolean, Float, DateTime, Date, Field, Relationship, SQLModel
import uuid

class MessageTransportLog(SQLModel):

    message_id: Optional[int] = Field(foreign_key="messages.id", index=True)

    mail_message_id: Optional[str] = Field(nullable=True)

    timestamp: datetime.datetime = Field(index=True)

    transport_host: str = Field(index=True, max_length=255)
    relay_host: str = Field(index=True, max_length=255)

    transport_type: str = Field(index=True, max_length=255)

    dsn: str = Field(index=True, max_length=25)
    dsn_message: str = Field(index=True)

    # TODO: In Django this was a models.DurationField. Need to look into what this is behind the scenes
    delay: int