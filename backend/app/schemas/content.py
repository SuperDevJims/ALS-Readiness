from pydantic import BaseModel, Field

from app.enums.content import ContentStatus, ContentType, ContentVisibility


class UploadUrlRequest(BaseModel):
    filename: str


class UploadUrlResponse(BaseModel):
    upload_url: str
    file_key: str


class ContentCreate(BaseModel):
    pass


class ContentResponse(BaseModel):
    id: int
    file_key: str
    title: str
    description: str | None
    type: ContentType
    status: ContentStatus
    visibility: ContentVisibility
    
