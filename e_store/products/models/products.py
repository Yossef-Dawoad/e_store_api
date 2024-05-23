from sqlmodel import Field, Relationship, SQLModel

from e_store.products.models.categories import Category, CategoryPublic


class ProductBase(SQLModel):  # hero
    name: str = Field(index=True)
    descriptions: str
    price: float
    quantity: int

    # TODO handle ondelete op
    category_id: int | None = Field(default=None, foreign_key="category.id")


class Product(ProductBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    category: Category | None = Relationship(back_populates="products")


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
    category: CategoryPublic | None = None
