from backend.app.models.learning_strand import Lesson

from .base import BaseRepository


class LessonRepository(BaseRepository[Lesson]):
    model = Lesson
