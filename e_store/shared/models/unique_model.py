from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class SimpleIDModel(SQLModel):
    id: int | None = Field(default=None, primary_key=True)


class UUIDIDModel(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
