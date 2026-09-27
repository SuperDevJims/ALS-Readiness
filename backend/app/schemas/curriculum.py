# app/schemas/curriculum.py
from pydantic import BaseModel

from app.enums.content import ContentType, StimulusLevel


class ContentNode(BaseModel):
    content_id: int
    title: str
    content_type: ContentType
    stimulus_level: StimulusLevel | None
    progress_status: str


class LessonNode(BaseModel):
    lesson_id: int
    title: str
    contents: list[ContentNode]


class ModuleNode(BaseModel):
    module_id: int
    title: str
    lessons: list[LessonNode]


class CurriculumResponse(BaseModel):
    strand_id: int
    strand_code: str
    strand_name: str
    strand_description: str
    modules: list[ModuleNode]