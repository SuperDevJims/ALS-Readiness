from app.models.test_item_asset import TestItemAsset

from .base import BaseRepository


class TestItemAssetRepository(BaseRepository[TestItemAsset]):
    model = TestItemAsset
