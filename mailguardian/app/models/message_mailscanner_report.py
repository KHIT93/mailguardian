from typing import Optional

from sqlmodel import Relationship

from mailguardian.app.models.base import BaseModel
from mailguardian.app.schemas.message_mailscanner_report import (
    MessageMailScannerReport as MessageMailScannerReportSchema,
)


class MessageMailScannerReport(MessageMailScannerReportSchema, BaseModel, table=True):
    __tablename__ = 'message_mailscanner_reports'

    message: Optional["Message"] = Relationship(back_populates='mailscanner_reports')  # type: ignore # noqa: F821
