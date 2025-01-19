from sqlmodel import Session

from mailguardian.database.connect import engine

class Environment:
    db: Session

    def __init__(self):
        self._init_database_session()

    def _init_database_session(self):
        self.db = Session(engine)