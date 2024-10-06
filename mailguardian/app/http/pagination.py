from typing import Optional

from sqlalchemy import Select, func
from sqlmodel import Session, select

from mailguardian.app.http.middleware import request_object
from mailguardian.database.connect import engine

class Paginator:
    def __init__(self, session: Session, query: Select, page: int, per_page: int = 20):
        self.session = session
        self.query = query
        self.page = page
        self.per_page = per_page
        self.limit = per_page * page
        self.offset = (page - 1) * per_page
        self.request = request_object.get()
        # computed later
        self.number_of_pages = 0
        self.next_page = ''
        self.previous_page = ''

    def _get_next_page(self) -> Optional[str]:
        if self.page >= self.number_of_pages:
            return
        url = self.request.url.include_query_params(page=self.page + 1)
        return str(url)

    def _get_previous_page(self) -> Optional[str]:
        if self.page == 1 or self.page > self.number_of_pages + 1:
            return
        url = self.request.url.include_query_params(page=self.page - 1)
        return str(url)

    async def get_response(self) -> dict:
        return {
            'count': await self._get_total_count(),
            'next_page': self._get_next_page(),
            'previous_page': self._get_previous_page(),
            'items': [item for item in self.session.scalars(self.query.limit(self.limit).offset(self.offset))]
        }

    def _get_number_of_pages(self, count: int) -> int:
        rest = count % self.per_page
        quotient = count // self.per_page
        return quotient if not rest else quotient + 1

    async def _get_total_count(self) -> int:
        count = self.session.scalar(select(func.count()).select_from(self.query.subquery()))
        self.number_of_pages = self._get_number_of_pages(count)
        return count


async def paginate(query: Select, page: int, per_page: int = 20) -> dict:
    with Session(engine) as session:
        paginator = Paginator(session, query, page, per_page)
        return await paginator.get_response()