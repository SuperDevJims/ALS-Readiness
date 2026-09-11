from app.models.strand_test import StrandTestItem

from .base import BaseRepository


class StrandTestItemRepository(BaseRepository[StrandTestItem]):
    model = StrandTestItem
