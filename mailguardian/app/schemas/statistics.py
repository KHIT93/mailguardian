import datetime
import enum
from typing import Any, Literal, TypeVar, Generic
from pydantic import BaseModel

from mailguardian.app.models.message import Message

T = TypeVar('T')

class FilterOperator(enum.Enum):
    EQUAL = '='
    NOT_EQUAL = '!='
    GREATER_THAN = '>'
    LESS_THAN = '<'
    CONTAINS = 'in'
    NOT_CONTAINS = 'not in'

class StatisticsResponse(BaseModel, Generic[T]):
    total: int
    first_date: datetime.date | None
    last_date: datetime.date | None
    items: list[T]

class MessageStatistics(StatisticsResponse[Message]):
    pass

class MessageFilter(BaseModel):
    field: str
    operator: FilterOperator
    value: Any