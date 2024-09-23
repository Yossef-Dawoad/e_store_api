from datetime import datetime
from typing import TYPE_CHECKING, ClassVar, Optional

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel, String

from e_store.shared.models.time_stamp_models import CreateUpdateAtTimestamp

if TYPE_CHECKING:
    from e_store.cart.models import Cart
    from e_store.orders.models import Order

    from .address import Address


class UserBase(SQLModel):
    username: str = Field(index=True, min_length=3)
    email: EmailStr = Field(unique=True, index=True, sa_type=String(255))
    disabled: bool | None = None


# TODO add SimpleTimeMixin to User
class User(UserBase, CreateUpdateAtTimestamp, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str = Field(min_length=8)
    verified_at: datetime | None = None  # TODO Run Migration for verified_at

    cart: Optional["Cart"] = Relationship(back_populates="user")
    addresses: list["Address"] = Relationship(back_populates="user")
    orders: list["Order"] = Relationship(back_populates="user")

    def create_hashed_ctx(self, context: str) -> str:
        return f"{context}{self.hashed_password[:-6]}{self.updated_at.strftime("%m%d%Y%H%M%S")}".strip()


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class UserPublic(UserBase):
    id: int


class UserUpdate(SQLModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None


class UserPublicWithAddresses(UserPublic):
    addresses: ClassVar[list["Address"]] = []
