from sqlmodel import Field, SQLModel


class MessageSpamReport(SQLModel):
    message_id: int | None = Field(foreign_key="messages.id", index=True)
    rule: str
    score: float
