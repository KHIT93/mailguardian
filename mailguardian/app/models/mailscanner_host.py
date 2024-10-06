from mailguardian.app.models.base import BaseModel
from mailguardian.app.schemas.mailscanner_host import MailScannerHost as MailScannerHostSchema
from mailguardian.config.app import settings
from typing import TYPE_CHECKING, Optional, Literal
from pathlib import Path
from pydantic import UUID4, EmailStr, IPvAnyAddress, AwareDatetime
from ipaddress import IPv4Address, IPv6Address
from sqlmodel import Column, ForeignKey, Uuid, Integer, String, Boolean, Float, DateTime, Date, Field
import uuid

class MailScannerHost(MailScannerHostSchema, BaseModel, table=True):
    __tablename__ = 'mailscanner_hosts'
    