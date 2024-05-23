from sqlmodel import Field, Relationship, SQLModel


class CategoryBase(SQLModel):  # team
    name: str = Field(index=True, min_length=2, max_length=60)


class Category(CategoryBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    products: list["Product"] = Relationship(back_populates="category")  # type: ignore # noqa: F821


class CategoryCreate(CategoryBase):
    pass


class CategoryPublic(CategoryBase):
    id: int


class CategoryPublicWithProducts(CategoryPublic):
    products: list["ProductPublic"] = []  # type: ignore # noqa: RUF012, F821
