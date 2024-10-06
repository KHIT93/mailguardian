from mailguardian.app.models.base import BaseModel
from mailguardian.app.schemas.spamassassin_rule_description import SpamAssassinRuleDescription as SpamAssassinRuleDescriptionSchema
from mailguardian.config.app import settings
from typing import TYPE_CHECKING, Optional, Literal
from pathlib import Path
from pydantic import UUID4, EmailStr, IPvAnyAddress, AwareDatetime
from sqlmodel import Column, ForeignKey, Uuid, Integer, String, Boolean, Float, DateTime, Date, Field
import uuid

class SpamAssassinRuleDescription(SpamAssassinRuleDescriptionSchema, BaseModel, table=True):
    __tablename__ = 'spamassassin_rule_descriptions'
