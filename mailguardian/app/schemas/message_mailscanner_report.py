from sqlmodel import Field, SQLModel


class MessageMailScannerReport(SQLModel):
    message_id: int | None = Field(foreign_key="messages.id", index=True)
    contents: str
