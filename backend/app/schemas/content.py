from pydantic import BaseModel, ConfigDict

from app.enums.content import (
    ContentStatus,
    ContentType,
    ContentVisibility,
    StimulusLevel,
)


class UploadUrlRequest(BaseModel):
    filename: str


class UploadUrlResponse(BaseModel):
    upload_url: str
    file_key: str


class ContentCreate(BaseModel):
    lesson_id: int
    file_key: str
    title: str
    description: str | None = None
    visibility: ContentVisibility = ContentVisibility.PRIVATE


class ContentResponse(BaseModel):
    id: int
    file_key: str
    title: str
    description: str | None
    type: ContentType
    status: ContentStatus
    visibility: ContentVisibility

    model_config = ConfigDict(from_attributes=True)


class ContentEvaluationCreate(BaseModel):
    stimulus_level: StimulusLevel
    cognitive_sustainability_rating: float


class ContentEvaluationResultResponse(BaseModel):
    stimulus_level: StimulusLevel
    cognitive_sustainability_rating: float


class ContentEvaluationResponse(BaseModel):
    id: int
    content_id: int
    stimulus_level: StimulusLevel
    cognitive_sustainability_rating: float

    model_config = ConfigDict(from_attributes=True)
