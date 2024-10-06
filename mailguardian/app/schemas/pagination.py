from fastapi import Query
from pydantic import AnyHttpUrl, BaseModel, Field
from typing import Optional, Generic, TypeVar, List

M = TypeVar('M')

class PaginatedParams:
    def __init__(self, page: int = Query(1, ge=1), per_page: int = Query(50, ge=0)):
        self.limit = per_page * page
        self.offset = (page - 1) * per_page

class PaginatedResponse(BaseModel, Generic[M]):
    count: int = Field(description='Number of total items')
    items: List[M] = Field(description='List of items returned in a paginated response')
    next_page: Optional[AnyHttpUrl] = Field(None, description='url of the next page if it exists')
    previous_page: Optional[AnyHttpUrl] = Field(None, description='url of the previous page if it exists')