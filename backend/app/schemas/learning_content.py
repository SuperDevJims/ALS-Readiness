from pydantic import BaseModel

from app.enums.content import ContentStatus


class ContentUpdate(BaseModel):
    status: ContentStatus 