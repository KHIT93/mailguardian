import datetime
from mailguardian.app.models.base import BaseModel
from mailguardian.app.schemas.message import Message as MessageSchema
from mailguardian.config.app import settings
from typing import TYPE_CHECKING, Optional, List
from pathlib import Path
from pydantic import EmailStr, IPvAnyAddress, AwareDatetime
from sqlmodel import Column, ForeignKey, Uuid, Integer, String, Boolean, Float, DateTime, Date, Field, Relationship
import uuid

class Message(MessageSchema, BaseModel, table=True):
    __tablename__ = 'messages'

    mailscanner_reports: List["MessageMailScannerReport"] = Relationship(back_populates='message')
    rbl_reports: List["MessageRblReport"] = Relationship(back_populates='message')
    mcp_reports: List["MessageMcpReport"] = Relationship(back_populates='message')
    spam_reports: List["MessageSpamReport"] = Relationship(back_populates='message')
    headers: List["MessageHeader"] = Relationship(back_populates='message')
    transport_logs: List["MessageTransportLog"] = Relationship(back_populates='message')
