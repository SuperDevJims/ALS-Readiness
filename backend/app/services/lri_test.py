from app.core.exceptions import LRITestNotFoundError
from app.enums.attempt import AttemptStatus
from app.models.lri_test import LRITest
from app.repositories.lri_test import LRITestRepository
from app.schemas.lri_test import (
    LRITestItemResponse,
    LRITestWithAttemptStatusResponse,
    LRITestWithItemsResponse,
)

from .learner import LearnerService


class LRITestService:
    def __init__(self, test_repository: LRITestRepository, learner_service: LearnerService):
        self._test_repository = test_repository
        self._learner_service = learner_service

    async def get_by_id(self, test_id: int) -> LRITest:
        test = await self._test_repository.get_by_id(test_id)

        if test is None:
            raise LRITestNotFoundError()

        return test

    async def get_with_attempt_status(self, user_id) -> LRITestWithAttemptStatusResponse:
        learner = await self._learner_service.get_by_user_id(user_id)

        consolidated_data = await self._test_repository.get_with_attempt(learner.id)

        if not consolidated_data:
            raise LRITestNotFoundError()

        test, test_attempt = consolidated_data

        return LRITestWithAttemptStatusResponse(
            test_id=test.id,
            title=test.title,
            description=test.description,
            attempt_status=AttemptStatus.COMPLETED if test_attempt is not None else AttemptStatus.PENDING
        )

    async def get_by_id_with_items(self, test_id: int):
        consolidated_data = await self._test_repository.get_by_id_with_items(test_id)

        if not consolidated_data:
            raise LRITestNotFoundError()

        items = []

        for data in consolidated_data:
            _, item = data

            items.append(
                LRITestItemResponse(
                    item_id=item.id,
                    question_text=item.question_text
                )
            )

        test = consolidated_data[0][0]

        return LRITestWithItemsResponse(
            test_id=test.id,
            title=test.title,
            description=test.description,
            items=items
        )
