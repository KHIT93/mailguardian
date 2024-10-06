from mailguardian.app.models.base import BaseModel
from mailguardian.app.schemas.user import User as UserSchema
from mailguardian.app.models.many2many import UserDomain
from mailguardian.config.app import settings, TOKEN_ALGORITHM
from pydantic import EmailStr, field_validator, validator
from typing import TYPE_CHECKING, List
from sqlmodel import Column, ForeignKey, Uuid, Integer, String, Boolean, Field, Relationship, select
import importlib
import uuid

# from app.auth.utils import hash_password

class User(UserSchema, BaseModel, table=True):
    __tablename__ = 'users'

    password: str = Field(exclude=True)

    domains: List["Domain"] = Relationship(link_model=UserDomain, back_populates='users')
