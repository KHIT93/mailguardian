from sqlmodel import Field, SQLModel


class SpamAssassinRuleDescription(SQLModel):
    key: str = Field(max_length=255, unique=True)
    value: str = Field(unique=True)
