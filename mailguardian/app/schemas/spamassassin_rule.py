from sqlmodel import Field, SQLModel


class SpamAssassinRule(SQLModel):
    name: str = Field(max_length=255, unique=True)
    score: float = Field(default=0.00)
