from uuid import UUID, uuid4

from pydantic import BaseModel
from sqlmodel import Field


class SimpleIDModel(BaseModel):
    id: int


class UUIDIDModel(BaseModel):
    id: UUID = Field(default_factory=uuid4)
