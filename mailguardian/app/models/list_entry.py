from mailguardian.app.models.base import BaseModel
from mailguardian.app.schemas.list_entry import ListEntry as ListEntrySchema


class ListEntry(ListEntrySchema, BaseModel, table=True):
    __tablename__ = 'list_entries'
