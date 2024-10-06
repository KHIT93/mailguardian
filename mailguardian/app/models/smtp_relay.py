from mailguardian.app.models.base import BaseModel
from mailguardian.app.schemas.smtp_relay import SmtpRelay as SmtpRelaySchema
from mailguardian.config.app import settings
from typing import TYPE_CHECKING, Optional
from pathlib import Path
from pydantic import UUID4, EmailStr, IPvAnyAddress, AwareDatetime
from sqlmodel import Column, ForeignKey, Uuid, Integer, String, Boolean, Float, DateTime, Date, Field
import uuid

class SmtpRelay(SmtpRelaySchema, BaseModel, table=True):
    __tablename__ = 'smtp_relays'