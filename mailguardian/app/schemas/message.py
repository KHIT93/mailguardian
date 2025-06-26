import datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel
from sqlmodel import Field, SQLModel

from mailguardian.config.app import settings


class Message(SQLModel):

    from_address: str | None = Field(nullable=True, index=True, default='')
    from_domain: str | None = Field(nullable=True, index=True, default='')

    to_address: str | None = Field(nullable=True, index=True, default='')
    to_domain: str | None = Field(nullable=True, index=True, default='')

    subject: str | None = Field(nullable=True, index=True, default='')

    client_ip: str | None = Field(nullable=True, index=True)

    mailscanner_hostname: str = Field(index=True, max_length=255)

    spam_score: float = Field(default=0.00)
    mcp_score: float = Field(default=0.00)

    timestamp: datetime.datetime = Field(index=True)

    date: datetime.date = Field(index=True)
    size: float = Field(default=0.0)
    token: str = Field(nullable=True)

    mailq_id: str = Field(nullable=True)
    mail_message_id: str = Field(nullable=True)

    allowed: bool = Field(index=True, default=False)
    blocked: bool = Field(index=True, default=False)

    is_spam: bool = Field(index=True, default=False)
    is_mcp: bool = Field(index=True, default=False)
    is_rbl_listed: bool = Field(index=True, default=False)

    stored: bool = Field(index=True, default=False)
    infected: bool = Field(index=True, default=False)
    scanned: bool = Field(index=True, default=False)

    def __str__(self) -> str:
        return str(self.id) + "[" + str(self.from_address) + " to " + str(self.to_address) + "]"

    def file_path(self) -> Path | None:
        if self.mailq_id:
            folder = 'nonspam' if not self.is_spam else 'spam'
            return Path(settings.MAILSCANNER_QUARANTINE_DIR, datetime.date.strftime(self.date, '%Y%m%d'), folder, self.mailq_id)
        else:
            return None

    def queue_file_exists(self) -> bool:
        file_path = self.file_path()
        return file_path and file_path.is_file()


class MessageDetail(BaseModel):
    body: str
    attachments: list[str] = []


class ProcessableMessage(BaseModel):
    qid: str
    size: int
    parsed: bool
    parse_error: str
    date: datetime.datetime
    status: str
    sender: str
    recipients: list[str]
    errors: list[str]
    errors: Any
    postcat_cmd: Any


class MessageProcessingQueue(BaseModel):
    messages: list[ProcessableMessage]
