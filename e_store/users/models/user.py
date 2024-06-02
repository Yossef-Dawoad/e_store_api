from typing import TYPE_CHECKING, ClassVar, Optional

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel, String

if TYPE_CHECKING:
    from e_store.cart.models import Cart
    from e_store.orders.models import Order

    from .address import Address


class UserBase(SQLModel):
    username: str = Field(index=True, min_length=3)
    email: EmailStr = Field(unique=True, index=True, sa_type=String(255))
    disabled: bool | None = None


# TODO add SimpleTimeMixin to User
class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str = Field(min_length=8)

    cart: Optional["Cart"] = Relationship(back_populates="user")
    addresses: list["Address"] = Relationship(back_populates="user")
    orders: list["Order"] = Relationship(back_populates="user")


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
