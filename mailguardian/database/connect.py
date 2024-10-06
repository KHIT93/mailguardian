from contextlib import contextmanager
from mailguardian.config.app import settings
from sqlmodel import create_engine, SQLModel, Session
import logging
logger = logging.getLogger(__name__)

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True, echo=False)

class Database:
    def __init__(self) -> None:
        pass
    @contextmanager
    def session(self):
        with Session(engine) as session:
            yield session