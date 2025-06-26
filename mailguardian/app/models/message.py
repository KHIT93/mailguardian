from sqlmodel import Relationship

from mailguardian.app.models.base import BaseModel
from mailguardian.app.schemas.message import Message as MessageSchema


class Message(MessageSchema, BaseModel, table=True):
    __tablename__ = 'messages'

    mailscanner_reports: list["MessageMailScannerReport"] = Relationship(back_populates='message')  # type: ignore # noqa: F821
    rbl_reports: list["MessageRblReport"] = Relationship(back_populates='message')  # type: ignore # noqa: F821
    mcp_reports: list["MessageMcpReport"] = Relationship(back_populates='message')  # type: ignore # noqa: F821
    spam_reports: list["MessageSpamReport"] = Relationship(back_populates='message')  # type: ignore # noqa: F821
    headers: list["MessageHeader"] = Relationship(back_populates='message')  # type: ignore # noqa: F821
    transport_logs: list["MessageTransportLog"] = Relationship(back_populates='message')  # type: ignore # noqa: F821
