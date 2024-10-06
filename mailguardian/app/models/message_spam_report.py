import datetime
from mailguardian.app.models.base import BaseModel
from mailguardian.app.schemas.message_spam_report import MessageSpamReport as MessageSpamReportSchema
from mailguardian.config.app import settings
from typing import TYPE_CHECKING, Optional
from pathlib import Path
from pydantic import UUID4, EmailStr, IPvAnyAddress, AwareDatetime
from sqlmodel import Column, ForeignKey, Uuid, Integer, String, Boolean, Float, DateTime, Date, Field, Relationship
import uuid

class MessageSpamReport(MessageSpamReportSchema, BaseModel, table=True):
    __tablename__ = 'message_spam_reports'

    message: Optional["Message"] = Relationship(back_populates='spam_reports')