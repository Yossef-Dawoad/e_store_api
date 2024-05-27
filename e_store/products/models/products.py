from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from e_store.cart.models import CartItem
    from e_store.orders.models import OrderDetail

    from .categories import Category, CategoryPublic


class ProductBase(SQLModel):  # hero
    name: str = Field(index=True)
    descriptions: str
    price: float
    quantity: int
    # TODO add `image_url` as String

    # TODO handle ondelete op
    category_id: int | None = Field(default=None, foreign_key="category.id")


class Product(ProductBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    category: Optional["Category"] = Relationship(back_populates="products")
    cart_items: list["CartItem"] = Relationship(back_populates="products")
    order_detail: Optional["OrderDetail"] = Relationship(back_populates="product")


class ProductPublic(ProductBase):
    id: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(SQLModel):
    name: str | None = None
    descriptions: str | None = None
    price: float | None = None
    quantity: int | None = None
    category_id: int | None = None


class ProductPublicWithCategory(ProductPublic):
    category: Optional["CategoryPublic"] = None
