import logging
from abc import ABC, abstractmethod
from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy import Engine
from sqlmodel import Session, create_engine

from mailguardian.config.app import settings

logger = logging.getLogger(__name__)

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI.unicode_string(),
    pool_pre_ping=True,
    echo=False
)


class DatabaseProtocol(ABC):
    @abstractmethod
    def get_session(self) -> Session:
        """
        Retrieves or creates a new database session.

        If the session attribute is None, it initializes a new SQLAlchemy
        session using the engine and returns it. Otherwise, it simply returns
        the existing session.

        Returns:
            Session: The current or newly created SQLAlchemy session.
        """
        pass

    @abstractmethod
    def close_session(self) -> None:
        """
        Closes the current database session if it exists.

        This method is used to release the connection associated with
        the SQLAlchemy session back to the connection pool and set the
        session attribute to None.
        """
        pass

    @abstractmethod
    @contextmanager
    def session_scope(self) -> Generator[Session, None, None]:
        """
        Context manager for managing a database session.

        This method provides a context in which to use the session.
        It ensures that the session is committed if no exceptions occur,
        rolled back in case of any exceptions, and finally closes the session.
        Yields:
            Session: The SQLAlchemy session within the scope.

        Raises:
            Exception: If an exception occurs during the transaction.
        """
        pass


class Database(DatabaseProtocol):
    """
    Database class provides an interface for managing database sessions and transactions.
    It follows the DatabaseProtocol and uses SQLAlchemy for session management.

    Attributes:
        engine (Engine): The SQLAlchemy engine used to create sessions.
        _session (Optional[Session]): The current active session, if any.

    Methods:
        close_session: Closes the current database session if it exists.
        get_session: Retrieves or creates a new database session.
        session_scope: Context manager for managing a database session.
    """
    def __init__(self):
        self.engine: Engine = create_engine(settings.SQLALCHEMY_DATABASE_URI.unicode_string(), pool_pre_ping=True, echo=False)
        self._session: Session | None = None

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
