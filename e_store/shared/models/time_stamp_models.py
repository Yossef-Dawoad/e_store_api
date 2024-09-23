from datetime import UTC, datetime

from sqlmodel import DateTime, Column, Field, SQLModel, func


class SimpleTimeStamp(SQLModel):
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class CreateUpdateAtTimestamp(SimpleTimeStamp):
    updated_at: datetime | None = Field(
        sa_column=Column(DateTime, onupdate=func.now()),
    )


class EventTimestamp(SQLModel):
    occured_at: datetime | None
