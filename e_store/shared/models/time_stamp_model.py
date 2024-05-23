from datetime import UTC, datetime

from sqlmodel import DATETIME, Column, Field, SQLModel, func


class SimpleTimeStamp(SQLModel):
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class TimestampModel(SimpleTimeStamp):
    updated_at: datetime | None = Field(
        sa_column=Column(DATETIME, onupdate=func.now()),
    )


class EventTimestamp(SQLModel):
    occured_at: datetime | None
