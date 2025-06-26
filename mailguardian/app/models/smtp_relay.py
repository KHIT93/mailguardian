from mailguardian.app.models.base import BaseModel
from mailguardian.app.schemas.smtp_relay import SmtpRelay as SmtpRelaySchema


class SmtpRelay(SmtpRelaySchema, BaseModel, table=True):
    __tablename__ = 'smtp_relays'
