from sqlmodel import Field

from .base import BaseEntity


class Learner(BaseEntity, table=True):
    __tablename__ = "learners"

    user_id: int = Field(foreign_key="users.id", unique=True)
