from datetime import datetime

from sqlalchemy import func
from sqlmodel import Field, SQLModel


class BaseEntity(SQLModel):
    id: int | None = Field(primary_key=True) 


class TimestampMixin(SQLModel):
    created_at: datetime | None = Field(
        default=None, sa_column_kwargs={"server_default": func.now()}
    )

    updated_at: datetime | None = Field(
        default=None,
        sa_column_kwargs={
            "server_default": func.now(),
            "onupdate": func.now(),
        },
    )
