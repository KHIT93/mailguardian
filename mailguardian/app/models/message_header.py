from typing import Optional

from sqlmodel import Relationship

from mailguardian.app.models.base import BaseModel
from mailguardian.app.schemas.message_header import MessageHeader as MessageHeaderSchema


class MessageHeader(MessageHeaderSchema, BaseModel, table=True):
    __tablename__ = 'message_headers'

    message: Optional["Message"] = Relationship(back_populates='headers')  # type: ignore # noqa: F821
