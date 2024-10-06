from mailguardian.config.app import settings
from typing import TYPE_CHECKING, Optional, Literal
from pathlib import Path
from pydantic import UUID4, EmailStr, IPvAnyAddress, AwareDatetime
from ipaddress import IPv4Address, IPv6Address
from sqlmodel import Column, ForeignKey, Uuid, Integer, String, Boolean, Float, DateTime, Date, Field, SQLModel
import uuid

class MailScannerHost(SQLModel):

    hostname: str = Field(max_length=255)
    # ip_address: IPv4Address | IPv6Address = Field(index=True)
    ip_address: str = Field(index=True)
    use_tls: bool = Field(default=True)
    priority: int = Field(default=10)
    passive: bool = Field(default=False)
    