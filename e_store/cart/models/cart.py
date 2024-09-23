from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from e_store.products.models.products import ProductPublic
from e_store.shared.models import SimpleIDModel, SimpleTimeStamp

if TYPE_CHECKING:
    from e_store.products.models import Product
    from e_store.users.models.user import User


class CartItemBase(SQLModel):
    cart_id: int | None = Field(default=None, foreign_key="cart.id", primary_key=True)
    product_id: int | None = Field(default=None, foreign_key="product.id", primary_key=True)
    quantity: int = Field(default=1)
    subtotal: Decimal = Field(default=0.0)


class CartItem(CartItemBase, table=True):
    """A Link Table between Products & Carts"""

    cart: Optional["Cart"] = Relationship(back_populates="items")
    product: Optional["Product"] = Relationship(back_populates="cart_items")


class CartItemPublic(SQLModel):
    product: ProductPublic


class CartBase(SQLModel):
    user_id: int | None = Field(default=None, foreign_key="user.id")


class Cart(CartBase, SimpleIDModel, SimpleTimeStamp, table=True):
    total_amount: Decimal = Field(default=0.0, decimal_places=2)

    items: list["CartItem"] = Relationship(
        back_populates="cart",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
    user: Optional["User"] = Relationship(back_populates="cart")


class CartPublic(CartBase):
    id: int
    items: list[CartItemPublic] = []


class CartCreate(CartBase):
    pass
