from enum import Enum

from sqlmodel import Field, SQLModel


class ListingType(str, Enum):
    ALLOWED = 'allowed'
    BLOCKED = 'blocked'


class ListEntry(SQLModel):

    from_address: str = Field(nullable=False, index=True)
    from_domain: str | None = Field(nullable=True, index=True)

    to_address: str = Field(nullable=False, index=True)
    to_domain: str | None = Field(nullable=True, index=True)

    listing_type: ListingType = Field(index=True, max_length=12)
