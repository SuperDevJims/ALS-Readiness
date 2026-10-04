from app.core.exceptions import CurriculumModuleNotFoundError, LessonNotFoundError
from app.enums.curriculum import StructureStatus
from app.models.lesson import Lesson
from app.models.user import User
from app.repositories.lesson import LessonRepository
from app.repositories.module import ModuleRepository
from app.schemas.facilitator_curriculum import LessonCreate, LessonUpdate
from app.services.ordering import order_by_ids


class LessonService:
    """Lookup and authoring of a module's lessons. Structure is global per strand (D4)."""

    def __init__(self, lesson_repo: LessonRepository, module_repo: ModuleRepository):
        self._lesson_repo = lesson_repo
        self._module_repo = module_repo

    async def get_by_id(self, lesson_id: int) -> Lesson:
        lesson = await self._lesson_repo.get_by_id(lesson_id)

        if lesson is None:
            raise LessonNotFoundError()

        return lesson

    async def create(self, user: User, module_id: int, lesson_create: LessonCreate) -> Lesson:
        await self._ensure_module(module_id)

        # Placed last: after every existing lesson, archived ones included.
        order_index = await self._lesson_repo.get_max_order_index(module_id) + 1

        return await self._lesson_repo.create(
            Lesson(
                module_id=module_id,
                title=lesson_create.title,
                description=lesson_create.description,
                order_index=order_index,
                status=StructureStatus.ACTIVE,
                deleted_at=None,
                created_by=user.id,
            )
        )

    async def update(self, lesson_id: int, lesson_update: LessonUpdate) -> Lesson:
        lesson = await self.get_by_id(lesson_id)
        fields = lesson_update.model_dump(exclude_unset=True)

        # A restored lesson goes to the end of the list.
        if fields.get("status") == StructureStatus.ACTIVE and lesson.status != StructureStatus.ACTIVE:
            fields["order_index"] = await self._lesson_repo.get_max_order_index(lesson.module_id) + 1

        return await self._lesson_repo.update(lesson, fields)

    async def reorder(self, module_id: int, lesson_ids: list[int]) -> list[Lesson]:
        await self._ensure_module(module_id)

        active = [
            lesson
            for lesson in await self._lesson_repo.get_by_module_id(module_id)
            if lesson.status == StructureStatus.ACTIVE
        ]

        return await self._lesson_repo.set_order(order_by_ids(active, lesson_ids))

    async def _ensure_module(self, module_id: int) -> None:
        if await self._module_repo.get_by_id(module_id) is None:
            raise CurriculumModuleNotFoundError()
