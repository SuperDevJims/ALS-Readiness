from sqlalchemy import Enum as SQLEnum
from sqlmodel import Field

from app.enums.user import UserRole

from .base import BaseEntity, TimestampMixin


class User(BaseEntity, TimestampMixin, table=True):
    __tablename__ = "users"

    id_no: str | None = Field(max_length=20, unique=True, index=True)
    password_hash: str = Field(max_length=255)

    role: UserRole | None = Field(
        default=UserRole.LEARNER,
        sa_type=SQLEnum(
            UserRole,
            values_callable=lambda enum: [e.value for e in enum],
            name="user_role",
        ),
    )

    is_active: bool = Field(default=True)
