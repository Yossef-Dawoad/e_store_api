from typing import TYPE_CHECKING, Optional

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

    cart: "Cart" = Relationship(back_populates="cart_items")
    products: list["Product"] = Relationship(back_populates="cart_items")


class CartBase(SQLModel):
    user_id: int | None = Field(default=None, foreign_key="user.id")


class Cart(CartBase, SimpleIDModel, SimpleTimeStamp, table=True):
    cart_items: list["CartItem"] = Relationship(back_populates="cart")
    user: Optional["User"] = Relationship(back_populates="cart", sa_relationship_kwargs={"uselist": False})


class CartPublic(CartBase, SimpleTimeStamp):
    cart_items: list["CartItem"]


class CartCreate(CartBase):
    pass
