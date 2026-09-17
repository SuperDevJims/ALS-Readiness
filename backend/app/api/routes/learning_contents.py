from app.schemas.learning_content import ContentUpdate
from fastapi import APIRouter, Depends, File, UploadFile

router = APIRouter(
    prefix="/learning-contents",
    tags=["Learning Contents"]
)


@router.post("/evaluate")
def evaluate_content(content: Depends(UploadFile, File())):
    """
    Receives contents and delegates evaluation to TRIBE model, returning the resulting metrics to the client.
    """


@router.post("/upload")
def get_upload_url():
    """
    Hands over the Backblaze upload url base on the API key to client.
    """


@router.patch("/{content_id}")
def update_content_status(content_id: int, contentUpdate: ContentUpdate):
    """
    Update the content status of a learning content.
    """
