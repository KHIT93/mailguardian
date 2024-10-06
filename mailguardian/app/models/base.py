from pydantic import UUID4, ConfigDict
from typing import List
try:
    from typing import Self
except ImportError:
    from typing_extensions import Self
from typing import Optional
# from sqlalchemy.ext.declarative import as_declarative, declared_attr, declarative_base
# from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlmodel import SQLModel, Field, Session
from mailguardian.database.connect import engine
import uuid
from uuid import UUID

# Base = declarative_base()

class BaseModel(SQLModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    id: Optional[int] = Field(default=None, primary_key=True)
    # TODO: This gives an error as SQLModel cannot translate UUID4 to SQLAlchemy
    uuid: Optional[UUID] = Field(default_factory=uuid.uuid4, nullable=False, index=True)
    
    @classmethod
    def create(cls, values: dict) -> Self:
        instance = cls(**values)
        with Session(engine) as db:
            db.add(instance)
            db.commit()
            db.refresh(instance)
        return instance

    @classmethod
    def all(cls) -> List[Self]:
        with Session(engine) as db:
            return db.exec(cls).all()
    
    @classmethod
    def find(cls, id: UUID) -> Self:
        with Session(engine) as db:
            return db.get(cls, ident=id)
        
    @classmethod
    def findOrCreate(cls, id: UUID, values: dict) -> Self:
        return cls.find(id) or cls.create(values)