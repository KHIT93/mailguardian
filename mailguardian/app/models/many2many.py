from sqlmodel import Field, SQLModel
from typing import Optional
from pydantic import UUID4
from mailguardian.app.models.base import BaseModel

class UserDomain(SQLModel, table=True):
    __tablename__ = 'user_domains'
    domain_id: Optional[int] = Field(default=None, foreign_key='domains.id', primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key='users.id', primary_key=True)