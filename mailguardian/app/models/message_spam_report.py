from typing import Optional

from sqlmodel import Relationship

from mailguardian.app.models.base import BaseModel
from mailguardian.app.schemas.message_spam_report import (
    MessageSpamReport as MessageSpamReportSchema,
)


class MessageSpamReport(MessageSpamReportSchema, BaseModel, table=True):
    __tablename__ = 'message_spam_reports'

    message: Optional["Message"] = Relationship(back_populates='spam_reports')  # type: ignore # noqa: F821
