from sqlmodel import Field, SQLModel


class MessageHeader(SQLModel):
    message_id: int | None = Field(foreign_key="messages.id", index=True)
    key: str
    value: str
