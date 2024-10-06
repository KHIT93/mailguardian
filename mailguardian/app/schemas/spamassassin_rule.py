from mailguardian.config.app import settings
from typing import TYPE_CHECKING, Optional, Literal
from pathlib import Path
from pydantic import UUID4, EmailStr, IPvAnyAddress, AwareDatetime
from sqlmodel import Column, ForeignKey, Uuid, Integer, String, Boolean, Float, DateTime, Date, Field, SQLModel
import uuid

class SpamAssassinRule(SQLModel):

    name: str = Field(max_length=255, unique=True)
    score: float = Field(default=0.00)