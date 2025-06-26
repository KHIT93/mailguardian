from sqlalchemy import Select, func
from sqlmodel import select

from mailguardian.app.http.middleware import request_object
from mailguardian.app.service_providers.service_container import services
from mailguardian.database.connect import Database


class Paginator:
    def __init__(self, query: Select, page: int, per_page: int = 20):
        self.db = services.get(Database)
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

    def _get_next_page(self) -> str | None:
        if self.page >= self.number_of_pages:
            return
        url = self.request.url.include_query_params(page=self.page + 1)
        return str(url)

    def _get_previous_page(self) -> str | None:
        if self.page == 1 or self.page > self.number_of_pages + 1:
            return
        url = self.request.url.include_query_params(page=self.page - 1)
        return str(url)

    async def get_response(self) -> dict:
        return {
            'count': await self._get_total_count(),
            'next_page': self._get_next_page(),
            'previous_page': self._get_previous_page(),
            'items': list(self.db.get_session().scalars(self.query.limit(self.limit).offset(self.offset)))
        }

    def _get_number_of_pages(self, count: int) -> int:
        rest = count % self.per_page
        quotient = count // self.per_page
        return quotient if not rest else quotient + 1

    async def _get_total_count(self) -> int:
        count = self.db.get_session().scalar(select(func.count()).select_from(self.query.subquery()))
        self.number_of_pages = self._get_number_of_pages(count)
        return count


# async def paginate(query: Select, page: int, per_page: int = 20) -> dict:
#     with Session(engine) as session:
#         paginator = Paginator(session, query, page, per_page)
#         return await paginator.get_response()

async def paginate(query: Select, page: int, per_page: int = 20) -> dict:
    paginator = Paginator(query, page, per_page)
    return await paginator.get_response()

# async def paginate(query: Select, page: int, per_page: int = 20) -> dict:
#     with services.get(Database).session_scope() as session:
#         paginator = Paginator(session, query, page, per_page)
#         return await paginator.get_response()

# @inject_dependencies()
# async def paginate(db_connection: Annotated[Database, Depends()], query: Select, page: int, per_page: int = 20) -> dict:
#     with db_connection.session_scope() as session:
#         paginator = Paginator(session, query, page, per_page)
#         return await paginator.get_response()
