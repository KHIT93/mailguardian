from mailguardian.app.models.base import BaseModel
from mailguardian.app.schemas.domain import Domain as DomainSchema
from mailguardian.app.models.many2many import UserDomain
from datetime import datetime
import logging
from pydantic import UUID4, EmailStr, AwareDatetime
from typing import TYPE_CHECKING, List, Optional, Literal
from sqlalchemy import event
from sqlmodel import Field, Relationship, DateTime, insert
from sqlalchemy.engine.base import Connection
from sqlalchemy.orm.events import MapperEvents
from sqlalchemy.orm import Mapper

import uuid

_logger = logging.getLogger(__name__)

class Domain(DomainSchema, BaseModel, table=True):
    __tablename__ = 'domains'

    users: List["User"] = Relationship(back_populates='domains', link_model=UserDomain)

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