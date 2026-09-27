from app.models.lesson import Lesson

from .base import BaseRepository


class LessonRepository(BaseRepository[Lesson]):
    model = Lesson
