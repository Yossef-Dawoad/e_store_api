from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .user import User


class Address(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    street_name: str
    street_number: Optional[str]
    city: str
    state: Optional[str]
    country: str
    postal_code: Optional[int]

    user_id: int | None = Field(default=None, foreign_key="user.id")

    user: Optional["User"] = Relationship(back_populates="addresses")
