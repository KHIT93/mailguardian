from sqlmodel import Field, SQLModel


class UserDomain(SQLModel, table=True):
    __tablename__ = 'user_domains'
    domain_id: int | None = Field(default=None, foreign_key='domains.id', primary_key=True)
    user_id: int | None = Field(default=None, foreign_key='users.id', primary_key=True)
