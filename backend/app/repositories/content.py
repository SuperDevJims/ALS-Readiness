from app.models.content import Content

from .base import BaseRepository


class ContentRepository(BaseRepository[Content]):
    model = Content
