from typing import Optional

from sqlmodel import Relationship

from mailguardian.app.models.base import BaseModel
from mailguardian.app.schemas.message_mcp_report import (
    MessageMcpReport as MessageMcpReportSchema,
)


class MessageMcpReport(MessageMcpReportSchema, BaseModel, table=True):
    __tablename__ = 'message_mcp_reports'

    message: Optional["Message"] = Relationship(back_populates='mcp_reports')  # type: ignore # noqa: F821
