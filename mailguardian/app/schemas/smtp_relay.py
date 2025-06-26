from sqlmodel import Field, SQLModel


class SmtpRelay(SQLModel):
    ip_address: str = Field(max_length=255, index=True)
    hostname: str = Field(max_length=255, index=True, default='')
    active: bool = Field(default=False)
    comment: str | None = Field(default=None)
