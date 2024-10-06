import datetime
from mailguardian.app.models.base import BaseModel
from mailguardian.app.schemas.message_header import MessageHeader as MessageHeaderSchema
from mailguardian.config.app import settings
from typing import TYPE_CHECKING, Optional
from pathlib import Path
from pydantic import UUID4, EmailStr, IPvAnyAddress, AwareDatetime
from sqlmodel import Column, ForeignKey, Uuid, Integer, String, Boolean, Float, DateTime, Date, Field, Relationship
import uuid

class MessageHeader(MessageHeaderSchema, BaseModel, table=True):
    __tablename__ = 'message_headers'

    message: Optional["Message"] = Relationship(back_populates='headers')
