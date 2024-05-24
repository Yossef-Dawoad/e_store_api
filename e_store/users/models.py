from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlmodel import AutoString, Field, Relationship, SQLModel

if TYPE_CHECKING:
    from e_store.cart.models import Cart
    from e_store.orders.models import Order


class UserBase(SQLModel):
    name: str = Field(index=True, min_length=5)
    email: EmailStr = Field(
        unique=True,
        index=True,
        sa_type=AutoString,  # Specify sa_type
    )


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str = Field()

    cart: "Cart" | None = Relationship(back_populates="user")
    order: "Order" | None = Relationship(back_populates="user")


class UserCreate(UserBase):
    password: str


class UserPublic(UserBase):
    id: int


class UserUpdate(SQLModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None
