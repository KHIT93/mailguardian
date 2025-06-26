from typing import Optional

from sqlmodel import Relationship

from mailguardian.app.models.base import BaseModel
from mailguardian.app.schemas.message_rbl_report import (
    MessageRblReport as MessageRblReportSchema,
)


class MessageRblReport(MessageRblReportSchema, BaseModel, table=True):
    __tablename__ = 'message_rbl_reports'

    message: Optional["Message"] = Relationship(back_populates='rbl_reports')  # type: ignore # noqa: F821
