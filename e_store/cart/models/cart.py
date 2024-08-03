from decimal import Decimal
from typing import TYPE_CHECKING, ClassVar, Optional

from sqlmodel import Field, Relationship, SQLModel

from e_store.shared.models import SimpleIDModel, SimpleTimeStamp

if TYPE_CHECKING:
    from e_store.products.models import Product
    from e_store.users.models.user import User


class CartItem(SQLModel, table=True):
    """A Link Table between Products & Carts"""

    cart_id: int | None = Field(default=None, foreign_key="cart.id", primary_key=True)
    product_id: int | None = Field(default=None, foreign_key="product.id", primary_key=True)
    quantity: int = Field(default=0)
    subtotal: Decimal = Field(default=0.0)

    cart: Optional["Cart"] = Relationship(back_populates="cart_items")
    products: list["Product"] = Relationship(back_populates="cart_items")


class CartBase(SQLModel):
    user_id: int | None = Field(default=None, foreign_key="user.id")


class Cart(CartBase, SimpleIDModel, SimpleTimeStamp, table=True):
    total_amount: Decimal = Field(default=0.0, decimal_places=2)

    cart_items: list["CartItem"] = Relationship(back_populates="cart")
    user: Optional["User"] = Relationship(back_populates="cart")


class CartPublic(CartBase, SimpleTimeStamp):
    id: int


class CartPublicWithItems(CartPublic):
    cart_items: list["CartItem"] = []  # noqa: RUF012


class CartCreate(CartBase):
    pass
