from app.models.curriculum import Lesson

from .base import BaseRepository


class LessonRepository(BaseRepository[Lesson]):

    model = Lesson
