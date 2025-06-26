from mailguardian.app.models.base import BaseModel
from mailguardian.app.schemas.mailscanner_host import (
    MailScannerHost as MailScannerHostSchema,
)


class MailScannerHost(MailScannerHostSchema, BaseModel, table=True):
    __tablename__ = 'mailscanner_hosts'
