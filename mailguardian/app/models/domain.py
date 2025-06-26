import logging

from sqlmodel import Relationship

from mailguardian.app.models.base import BaseModel
from mailguardian.app.models.many2many import UserDomain
from mailguardian.app.schemas.domain import Domain as DomainSchema

_logger = logging.getLogger(__name__)


class Domain(DomainSchema, BaseModel, table=True):
    __tablename__ = 'domains'

    users: list["User"] = Relationship(back_populates='domains', link_model=UserDomain)  # type: ignore # noqa: F821

# @event.listens_for(Domain, "after_insert")
# def log_domain_creation(mapper: Mapper[Domain], connection: Connection, target: Domain) -> None:
#     _logger.info(f'{type(mapper)}: {mapper}')
#     _logger.info(f'{type(connection)}: {connection}')
#     _logger.info(f'{type(target)}: {target}')
#     # connection.execute(insert(Domain).values(
#     #     model=Domain.__class__,
#     #     res_id=target.id,
#     #     action='create',
#     #     actor_id=None,
#     #     acted_from='127.0.0.1',
#     #     changes=target.model_dump_json()
#     # ))
#     _logger.info(target.model_dump_json())
