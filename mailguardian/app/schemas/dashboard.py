import datetime
from pydantic import BaseModel

class TrafficGraph(BaseModel):
    date: datetime.date
    count: int

class SenderCount(BaseModel):
    domain: str
    count: int