import datetime
from functools import partial
from typing import Any, Optional, Union

from huey.api import Huey
from huey.constants import EmptyData
from huey.storage import BaseStorage
from sqlalchemy import ClauseElement
from sqlmodel import Session, delete, func, insert, select
from sqlalchemy.engine import Connection

from mailguardian.app.models.scheduler import KV, Schedule, Task
from mailguardian.database.connect import engine

def ensure_bytes(value: Union[str, bytes]) -> bytes:
    if isinstance(value, str):
        return value.encode()
    return value

class SQLModelStorage(BaseStorage):

    def create_models(self):
        return (KV, Schedule, Task)
    
    def create_tables(self):
        return True
    
    def drop_tables(self):
        return True
    
    def tasks(self, operation: Any = select, *columns: ClauseElement) -> Any:
        return operation(Task).where(Task.queue == self.name)
    
    def schedule(self, operation: Any = select, *columns: ClauseElement) -> Any:
        return operation(Schedule).where(Schedule.queue == self.name)
    
    def kv(self, operation: Any = select, *columns: ClauseElement) -> Any:
        return operation(KV).where(KV.queue == self.name)

    def enqueue(self, data: bytes, priority: Optional[float] = 0) -> int:
        with Session(engine) as db:
            task: Task = Task(queue=self.name, data=data, priority=priority)
            db.add(task)
            db.commit()
            db.refresh(task)
            return task.id
    
    def dequeue(self) -> bytes | None:

        query = self.tasks().with_for_update(skip_locked=True).order_by(Task.priority, Task.id)

        with Session(engine) as db:
            task: Task = db.exec(query).first()
            if not task:
                return
            
            task_data = task.data

            db.delete(task)
            db.commit()

            return task_data
    
    def queue_size(self) -> int:
        with Session(engine) as db:
            return len(db.exec(self.tasks()).all())

    def enqueued_items(self, limit:Optional[int]=None) -> list[bytes]:
        query = self.tasks().order_by(Task.priority, Task.id)

        if limit is not None:
            query = query.limit(limit)
        with Session(engine) as db:
            return [task.data for task in db.exec(query).all()]
    
    def flush_queue(self) -> None:
        with Session(engine) as db:
            db.exec(self.tasks(operation=delete))
            db.commit()

    def add_to_schedule(self, data: bytes, timestamp: datetime.datetime) -> None:
        with Session(engine) as db:
            schedule: Schedule = Schedule(queue=self.name, data=data, timestamp=timestamp)
            db.add(schedule)
            db.commit()

    def read_schedule(self, timestamp: datetime.datetime) -> list[bytes]:
        query = self.schedule().where(Schedule.timestamp <= timestamp).with_for_update(skip_locked=True)
        with Session(engine) as db:
            return [schedule.data for schedule in db.exec(query)]
    
    def schedule_size(self) -> int:
        with Session(engine) as db:
            return len(db.exec(self.schedule()).all())
    
    def scheduled_items(self, limit:Optional[int]=None) -> list[bytes]:
        query = self.schedule()

        if limit is not None:
            query = query.limit(limit)
        with Session(engine) as db:
            return [schedule.data for schedule in db.exec(query).all()]
    
    def flush_schedule(self) -> None:
        with Session(engine) as db:
            db.exec(self.schedule(operation=delete))
            db.commit()

    def put_data(self, key: bytes, value: bytes, is_result:bool=False) -> None:
        key = ensure_bytes(key)
        res: KV = self.kv().where(KV.key == key)
        with Session(engine) as db:
            res: KV = db.exec(self.kv().where(KV.key == key)).first()
            if not res:
                res = KV(queue=self.name, key=key, value=value)
            res.value = value
            db.add(res)
            db.commit()

    def peek_data(self, key: bytes) -> bytes | EmptyData:
        key = ensure_bytes(key)
        with Session(engine) as db:
            res: KV = db.exec(self.kv().where(KV.key == key)).first()
            if not res:
                return EmptyData
            if res.value is None:
                return EmptyData
            else:
                return res.value
    
    def pop_data(self, key: bytes) -> bytes | EmptyData:
        key = ensure_bytes(key)
        with Session(engine) as db:
            res: KV = db.exec(self.kv().where(KV.key == key)).first()
            if not res:
                return EmptyData

            data: bytes = res.value
            db.delete(res)
            db.commit()
            if data is None:
                return EmptyData
            else:
                return res.value
    
    def has_data_for_key(self, key: bytes) -> bool:
        key = ensure_bytes(key)
        with Session(engine) as db:
            return db.exec(self.kv().where(KV.key == key)).first() is not None
    
    def put_if_empty(self, key: bytes, value: bytes) -> bool:
        key = ensure_bytes(key)
        with Session(engine) as db:
            res: KV = KV(queue=self.name, key=key, value=value)
            db.add(res)
            db.commit()
            return True

    def result_store_size(self) -> int:
        with Session(engine) as db:
            return len(db.exec(self.kv()).all())
    
    def result_items(self)-> dict:
        with Session(engine) as db:
            return dict((r.key, r.value) for r in db.exec(self.kv()).all())

    def flush_results(self) -> None:
        with Session(engine) as db:
            db.exec(self.kv(operation=delete))

SqlHuey = partial(Huey, storage_class=SQLModelStorage)

queue = SqlHuey(name='MailGuardian', results=True, utc=True)