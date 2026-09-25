from app.schemas.content import (
    ContentCreate,
    ContentResponse,
    UploadUrlRequest,
    UploadUrlResponse,
)
from app.storage import build_key, get_upload_url
from fastapi import APIRouter, Depends, status

from ..deps import get_current_facilitator

router = APIRouter(
    prefix="/contents",
    tags=["Contents"],
    dependencies=[Depends(get_current_facilitator)],
)


@router.post("/upload-url", response_model=UploadUrlResponse)
async def create_upload_url(data: UploadUrlRequest):
    file_key = build_key("learning-contents", data.filename)
    upload_url = get_upload_url(file_key)

    return UploadUrlResponse(
        file_key=file_key,
        upload_url=upload_url,
    )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ContentResponse | None,
)
async def create_content(data: ContentCreate):
    pass
