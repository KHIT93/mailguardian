from mailguardian.app.models.base import BaseModel
from mailguardian.app.schemas.list_entry import ListEntry as ListEntrySchema
from mailguardian.config.app import settings
from typing import TYPE_CHECKING, Optional, Literal
from pathlib import Path
from pydantic import UUID4, EmailStr, IPvAnyAddress, AwareDatetime
from sqlmodel import Field, String, Column
import uuid

class ListEntry(ListEntrySchema, BaseModel, table=True):
    __tablename__ = 'list_entries'
