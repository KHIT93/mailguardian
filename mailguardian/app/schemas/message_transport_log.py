import datetime

from sqlmodel import Field, SQLModel


class MessageTransportLog(SQLModel):

    message_id: int | None = Field(foreign_key="messages.id", index=True)

    mail_message_id: str | None = Field(nullable=True)

    timestamp: datetime.datetime = Field(index=True)

    transport_host: str = Field(index=True, max_length=255)
    relay_host: str = Field(index=True, max_length=255)

    transport_type: str = Field(index=True, max_length=255)

    dsn: str = Field(index=True, max_length=25)
    dsn_message: str = Field(index=True)

    # TODO: In Django this was a models.DurationField. Need to look into what this is behind the scenes
    delay: int
