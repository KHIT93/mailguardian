import datetime
from enum import Enum
from pydantic import BaseModel, EmailStr
from typing import TYPE_CHECKING, List, Optional
from sqlmodel import Column, ForeignKey, Uuid, Integer, String, Boolean, Field, Relationship, SQLModel
import uuid

class UserRole(str, Enum):
    USER = 'user'
    DOMAIN_ADMINISTRATOR = 'domain_admin'
    SUPERUSER = 'superuser'

class PersonalDetails(SQLModel):
    email: str = Field(unique=True, index=True)
    first_name: Optional[str] = Field(nullable=True)
    last_name: Optional[str]= Field(nullable=True)

class User(PersonalDetails):
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
    session_id: uuid.UUID

class TotpScope(str, Enum):
    APP = 'app' # Short codes (6-8 digits) from a mobile app and with short lifetime (30 seconds)
    EMAIL = 'email' # Longer codes (8-10 digits) sent by email and with longer lifetime (5 minutes)

class TimeBasedCode(SQLModel):
    user_id: Optional[int] = Field(foreign_key="users.id", index=True)
    # scope: TotpScope = Field(default=TotpScope.APP)
    name: str
    created_at: datetime.datetime
    totp_secret: str

class TotpSetup(BaseModel):
    secret: str
    url: str

class TotpSetupVerification(TotpSetup):
    password: str
    code: str
    name: str

class RecoveryCode(SQLModel):
    user_id: Optional[int] = Field(foreign_key="users.id", index=True)
    code: str

class ChangePassword(BaseModel):
    current_password: str
    password: str
    confirm_password: str
    terminate_sessions: bool = Field(default=False)