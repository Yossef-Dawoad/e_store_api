from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from e_store.shared.models import SimpleIDModel, SimpleTimeStamp

if TYPE_CHECKING:
    from e_store.products.models.products import Product
    from e_store.users.models import User


class CartItemBase(SQLModel):
    cart_id: int | None = Field(default=None, foreign_key="cart.id")
    product_id: int | None = Field(default=None, foreign_key="product.id")


class CartItem(CartItemBase, SimpleIDModel, SimpleTimeStamp, table=True):
    cart: "Cart" | None = Relationship(back_populates="cart_items")
    products: list["Product"] = Relationship(back_populates="cart_items")


class CartBase(SQLModel):
    user_id: int | None = Field(default=None, foreign_key="user.id")


class Cart(CartBase, SimpleIDModel, SimpleTimeStamp, table=True):
    user: "User" | None = Relationship(back_populates="cart")
    cart_items: CartItem | None = Relationship(back_populates="cart")


class CartPublic(CartBase):
    id: int
    cart_items: list[CartItemBase]


class CartCreate(CartBase):
    pass
