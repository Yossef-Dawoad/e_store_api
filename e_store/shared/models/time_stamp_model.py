from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import DateTime, func
from sqlmodel import Column, Field


class SimpleTimeStamp(BaseModel):
    created_at: datetime = Field(default_factory=lambda: datetime.now(datetime.UTC))


class TimestampModel(SimpleTimeStamp):
    updated_at: datetime | None = Field(
        sa_column=Column(DateTime(), onupdate=func.now()),
    )


class EventTimestamp(BaseModel):
    occured_at: datetime | None
