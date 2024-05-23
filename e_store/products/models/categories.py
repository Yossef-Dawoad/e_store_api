from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .products import Product, ProductPublic


class CategoryBase(SQLModel):  # team
    name: str = Field(index=True, min_length=2, max_length=60)


class Category(CategoryBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    products: list["Product"] = Relationship(back_populates="category")


class CategoryCreate(CategoryBase):
    pass


class CategoryPublic(CategoryBase):
    id: int


class CategoryPublicWithProducts(CategoryPublic):
    products: list["ProductPublic"]
