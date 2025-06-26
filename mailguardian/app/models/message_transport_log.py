from typing import Optional

from sqlmodel import (
    Field,
    Relationship,
    SQLModel,
)

from mailguardian.app.models.base import BaseModel
from mailguardian.app.schemas.message_transport_log import (
    MessageTransportLog as MessageTransportLogSchema,
)


class MessageTransportLog(MessageTransportLogSchema, BaseModel, table=True):
    __tablename__ = 'message_transport_log'

    message: Optional["Message"] = Relationship(back_populates='transport_logs')  # type: ignore # noqa: F821


# This is magic join table for joining together all MessageTransportLog entries based on their mail_message_id
class MessageTransportIdentifier(SQLModel, table=True):
    __tablename__ = 'message_transport_log_ids'
    smtpd_id: str | None = Field(primary_key=True)
    smtp_id: str | None = Field(primary_key=True)
