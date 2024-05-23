from sqlmodel import Field, Relationship, SQLModel


class CategoryBase(SQLModel):  # team
    name: str = Field(index=True, min_length=2, max_length=60)


class Category(CategoryBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    products: list["Product"] = Relationship(back_populates="category")


class CategoryCreate(CategoryBase):
    pass


class CategoryPublic(CategoryBase):
    id: int


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
    price: int | None = None
    quantity: int | None = None
    category_id: int | None = None


class ProductPublicWithCategory(ProductPublic):
    category: CategoryPublic | None = None


class CategoryPublicWithProducts(CategoryPublic):
    products: list["ProductPublic"] = []  # noqa: RUF012
