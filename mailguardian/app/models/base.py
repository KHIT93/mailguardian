from pydantic import ConfigDict

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self
import uuid
from uuid import UUID

# from sqlalchemy.ext.declarative import as_declarative, declared_attr, declarative_base
# from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlmodel import Field, Session, SQLModel

from mailguardian.database.connect import engine

# Base = declarative_base()


class BaseModel(SQLModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    id: int | None = Field(default=None, primary_key=True)
    # TODO: This gives an error as SQLModel cannot translate UUID4 to SQLAlchemy
    uuid: UUID | None = Field(default_factory=uuid.uuid4, nullable=False, index=True)

    @classmethod
    def create(cls, values: dict) -> Self:
        instance = cls(**values)
        with Session(engine) as db:
            db.add(instance)
            db.commit()
            db.refresh(instance)
        return instance

    @classmethod
    def all(cls) -> list[Self]:
        with Session(engine) as db:
            return db.exec(cls).all()

    @classmethod
    def find(cls, id: UUID) -> Self:
        with Session(engine) as db:
            return db.get(cls, ident=id)

    @classmethod
    def findOrCreate(cls, id: UUID, values: dict) -> Self:
        return cls.find(id) or cls.create(values)
