from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class SimpleIDModel(SQLModel):
    id: int


class UUIDIDModel(SQLModel):
    id: UUID = Field(default_factory=uuid4)
