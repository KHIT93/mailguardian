from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Generator, Optional

from sqlalchemy import Engine
from mailguardian.config.app import settings
from sqlmodel import create_engine, SQLModel, Session
import logging
logger = logging.getLogger(__name__)

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI.unicode_string(),
    pool_pre_ping=True,
    echo=False
)

class DatabaseProtocol(ABC):
    @abstractmethod
    def get_session(self) -> Session:
        pass

    def close_session(self) -> None:
        pass

    @abstractmethod
    @contextmanager
    def session_scope(self) -> Generator[Session, None, None]:
        pass

class Database(DatabaseProtocol):
    def __init__(self):
        self.engine: Engine = create_engine(settings.SQLALCHEMY_DATABASE_URI.unicode_string(), pool_pre_ping=True, echo=False)
        self._session: Optional[Session] = None
    
    def close_session(self):
        if self._session is not None:
            self._session.close()
            self._session = None

    def get_session(self):
        if self._session is None:
            self._session = Session(self.engine)
        return self._session
    
    @contextmanager
    def session_scope(self) -> Generator[Session, None, None]:
        session = self.get_session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            self.close_session()