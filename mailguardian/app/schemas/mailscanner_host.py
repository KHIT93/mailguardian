from sqlmodel import Field, SQLModel


class MailScannerHost(SQLModel):

    hostname: str = Field(max_length=255)
    # ip_address: IPv4Address | IPv6Address = Field(index=True)
    ip_address: str = Field(index=True)
    use_tls: bool = Field(default=True)
    priority: int = Field(default=10)
    passive: bool = Field(default=False)
