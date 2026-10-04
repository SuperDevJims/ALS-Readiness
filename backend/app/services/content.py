from fastapi import UploadFile
from sqlalchemy.exc import IntegrityError

from app.core.exceptions import (
    ContentEvaluationAlreadyExistsError,
    ContentFileNotFoundError,
    ContentNotFoundError,
    InvalidContentFileError,
    StorageUnavailableError,
)
from app.enums.content import ContentStatus, ContentType, StimulusLevel
from app.models.content import Content
from app.models.content_evaluation import ContentEvaluation
from app.repositories.content import ContentRepository
from app.repositories.content_evaluation import ContentEvaluationRepository
from app.schemas.content import ContentCreate
from app.services.facilitator import FacilitatorService
from app.services.lesson import LessonService
from app.storage import STORAGE_ERRORS, build_key, file_exists, get_upload_url


class ContentService:
    ALLOWED_EXTENSIONS = {  # noqa: RUF012
        "mp4",
        "mov",
        "webm",
        "mp3",
        "wav",
        "m4a",
        "pdf",
        "txt",
        "docx",
    }

    def __init__(
        self,
        content_repo: ContentRepository,
        content_eval_repo: ContentEvaluationRepository,
        lesson_service: LessonService,
        facilitator_service: FacilitatorService,
    ):
        self._content_repo = content_repo
        self._content_eval_repo = content_eval_repo
        self._lesson_service = lesson_service
        self._facilitator_service = facilitator_service

    def _validate_extension(self, filename: str) -> None:
        if "." not in filename:
            raise InvalidContentFileError("Filename must include an extension")
        ext = filename.rsplit(".", 1)[-1].lower()
        if ext not in self.ALLOWED_EXTENSIONS:
            raise InvalidContentFileError(f"Unsupported file extension: .{ext}")

    def _derive_content_type(self, file_key: str) -> ContentType:
        if "." not in file_key:
            raise InvalidContentFileError("File key has no extension")

        ext = file_key.rsplit(".", 1)[-1].lower()
        if ext in {"mp4", "mov", "webm"}:
            return ContentType.VIDEO
        if ext in {"mp3", "wav", "m4a"}:
            return ContentType.AUDIO
        if ext in {"pdf", "txt", "docx"}:
            return ContentType.READING

        raise InvalidContentFileError(f"Unsupported file extension: .{ext}")

    def create_upload_url(self, filename: str) -> tuple[str, str]:
        self._validate_extension(filename)

        key = build_key("learning-contents", filename)
        try:
            upload_url = get_upload_url(key)
        except STORAGE_ERRORS:
            raise StorageUnavailableError() from None

        return key, upload_url

    async def create_content(
        self,
        user_id: int,
        content_create: ContentCreate,
    ) -> Content:
        facilitator = await self._facilitator_service.get_by_user_id(user_id)
        await self._lesson_service.get_active_by_id(content_create.lesson_id)

        try:
            exists = file_exists(content_create.file_key)
        except STORAGE_ERRORS:
            raise StorageUnavailableError() from None

        if not exists:
            raise ContentFileNotFoundError()

        content_type = self._derive_content_type(content_create.file_key)

        content = Content(
            **content_create.model_dump(),
            type=content_type,
            status=ContentStatus.ACTIVE,
            uploaded_by=facilitator.id,
        )

        return await self._content_repo.create(content)

    async def evaluate_content(self, file: UploadFile) -> tuple[StimulusLevel, float]:
        # Placeholder pending the TRIBE decision: the file is not read or
        # evaluated, and every call returns the same fixed result.
        return StimulusLevel.LOW, 0.5

    async def get_content_by_id(self, content_id: int) -> Content:
        content = await self._content_repo.get_by_id(content_id)

        if content is None:
            raise ContentNotFoundError()

        return content

    async def create_content_evaluation(
        self,
        content_id: int,
        stimulus_level: StimulusLevel,
        cognitive_sustainability_rating: float,
    ) -> ContentEvaluation:
        content = await self.get_content_by_id(content_id)

        # The unique constraint is the backstop; this check is what makes the
        # failure a clean 409.
        if await self._content_eval_repo.get_by_content_id(content.id) is not None:
            raise ContentEvaluationAlreadyExistsError()

        content_eval = ContentEvaluation(
            content_id=content.id,
            stimulus_level=stimulus_level,
            cognitive_sustainability_rating=cognitive_sustainability_rating,
        )

        try:
            return await self._content_eval_repo.create(content_eval)
        except IntegrityError:
            # A concurrent save got past the check above.
            raise ContentEvaluationAlreadyExistsError() from None
