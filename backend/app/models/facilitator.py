from sqlmodel import Field

from .base import BaseEntity


class Facilitator(BaseEntity, table=True):
    __tablename__ = "facilitators"

    user_id: int = Field(foreign_key="users.id", unique=True)
