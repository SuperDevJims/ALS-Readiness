from sqlmodel import Field

from .base import BaseEntity


class TestItemAsset(BaseEntity, table=True):
    __tablename__ = "test_item_assets"

    item_id: int = Field(foreign_key="strand_test_items.id")
    file_key: str
    content_type: str
