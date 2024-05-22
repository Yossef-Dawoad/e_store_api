from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    name: str = Field(index=True)
    email: str


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str = Field()


class UserCreate(UserBase):
    password: str


class UserPublic(UserBase):
    id: int


class UserUpdate(SQLModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None
