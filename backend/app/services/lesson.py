from fastapi import HTTPException

from app.models.lesson import Lesson
from app.repositories.lesson import LessonRepository


class LessonService:
    def __init__(self, lesson_repo: LessonRepository):
        self._lesson_repo = lesson_repo

    async def get_by_id(self, lesson_id: int) -> Lesson:
        lesson = await self._lesson_repo.get_by_id(lesson_id)

        if lesson is None:
            raise HTTPException(404, "Lesson does not exists.")
        
        return lesson