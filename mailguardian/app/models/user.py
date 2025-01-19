import datetime
from mailguardian.app.models.base import BaseModel
from mailguardian.app.schemas.user import User as UserSchema
from mailguardian.app.schemas.user import TimeBasedCode as TimeBasedCodeSchema
from mailguardian.app.schemas.user import RecoveryCode as RecoveryCodeSchema
from mailguardian.app.models.many2many import UserDomain
from mailguardian.config.app import settings, TOKEN_ALGORITHM
from pydantic import EmailStr, field_validator, validator
from typing import TYPE_CHECKING, List, Optional
from sqlmodel import Column, ForeignKey, Uuid, Integer, String, Boolean, Field, Relationship, select
import importlib
import uuid

# from app.auth.utils import hash_password

class User(UserSchema, BaseModel, table=True):
    __tablename__ = 'users'

    password: str = Field(exclude=True)

    created_at: datetime.datetime = Field(index=True, default_factory=datetime.datetime.now)

    domains: list["Domain"] = Relationship(link_model=UserDomain, back_populates='users')

    totp_codes: list["TimeBasedCode"] = Relationship(back_populates='user')

    sessions: list["UserSession"] = Relationship(back_populates='user')

class TimeBasedCode(TimeBasedCodeSchema, BaseModel, table=True):
    __tablename__ = 'totp_codes'
    user: Optional["User"] = Relationship(back_populates='totp_codes')

class RecoveryCode(RecoveryCodeSchema, BaseModel, table=True):
    __tablename__ = 'recovery_codes'

class UserSession(BaseModel, table=True):
    __tablename__ = 'sessions'
    user_id: Optional[int] = Field(foreign_key="users.id", index=True)
    user: Optional["User"] = Relationship(back_populates='sessions')
    created_at: datetime.datetime = Field(index=True, default_factory=datetime.datetime.now)
    expires_at: datetime.datetime = Field(index=True)