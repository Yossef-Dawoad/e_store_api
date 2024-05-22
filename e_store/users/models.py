from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    name: str = Field(index=True)
    email: str
    password: str


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class UserCreate(UserBase):
    pass
