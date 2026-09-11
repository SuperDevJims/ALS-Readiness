from app.models.lri_test import LRITestItem

from .base import BaseRepository


class LRITestItemRepository(BaseRepository[LRITestItem]):
    model = LRITestItem
