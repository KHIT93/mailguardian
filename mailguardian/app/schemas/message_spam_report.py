import datetime
from mailguardian.config.app import settings
from typing import TYPE_CHECKING, Optional
from pathlib import Path
from pydantic import UUID4, EmailStr, IPvAnyAddress, AwareDatetime
from sqlmodel import Column, ForeignKey, Uuid, Integer, String, Boolean, Float, DateTime, Date, Field, Relationship, SQLModel
import uuid

class MessageSpamReport(SQLModel):

    message_id: Optional[int] = Field(foreign_key="messages.id", index=True)
    rule: str
    score: float