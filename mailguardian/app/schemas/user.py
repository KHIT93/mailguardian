from enum import Enum
from pydantic import BaseModel, EmailStr
from typing import TYPE_CHECKING, List, Optional
from sqlmodel import Column, ForeignKey, Uuid, Integer, String, Boolean, Field, Relationship, SQLModel
import uuid

class UserRole(str, Enum):
    USER = 'user'
    DOMAIN_ADMINISTRATOR = 'domain_admin'
    SUPERUSER = 'superuser'

class User(SQLModel):

    email: str = Field(unique=True, index=True)
    first_name: Optional[str] = Field(nullable=True)
    last_name: Optional[str]= Field(nullable=True)

    is_active: bool = Field(default=True)

    role: UserRole = Field(default=UserRole.USER)

    @property
    def is_domain_admin(self):
        return self.role == UserRole.DOMAIN_ADMINISTRATOR
    
    @property
    def is_app_admin(self):
        return self.role == UserRole.SUPERUSER

class UserCreation(User):
    passwd: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
    role: UserRole = UserRole.USER