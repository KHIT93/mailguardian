import datetime
from mailguardian.app.models.base import BaseModel
from mailguardian.app.schemas.message_transport_log import MessageTransportLog as MessageTransportLogSchema
from mailguardian.config.app import settings
from typing import TYPE_CHECKING, Optional
from pathlib import Path
from pydantic import UUID4, EmailStr, IPvAnyAddress, AwareDatetime
from sqlmodel import Column, ForeignKey, Uuid, Integer, String, Boolean, Float, DateTime, Date, Field, Relationship, SQLModel
import uuid

class MessageTransportLog(MessageTransportLogSchema, BaseModel, table=True):
    __tablename__ = 'message_transport_log'

    message: Optional["Message"] = Relationship(back_populates='transport_logs')


# This is magic join table for joining together all MessageTransportLog entries based on their mail_message_id
class MessageTransportIdentifier(SQLModel, table=True):
    __tablename__ = 'message_transport_log_ids'
    smtpd_id: Optional[str] = Field(primary_key=True)
    smtp_id: Optional[str] = Field(primary_key=True)