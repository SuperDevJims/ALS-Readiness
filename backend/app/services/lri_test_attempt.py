from app.core.exceptions import InvalidTestAttemptError, LRITestAttemptNotFoundError
from app.models.lri_test_attempt import LRITestAttempt, LRITestAttemptAnswer
from app.repositories.lri_test_attempt import LRITestAttemptRepository
from app.repositories.lri_test_attempt_answer import LRITestAttemptAnswerRepository
from app.schemas.lri_test_attempt import (
    LRITestAttemptCreate,
    LRITestAttemptResponse,
    LRITestAttemptResultResponse,
)

from .learner import LearnerService
from .lri_test import LRITestService


class LRITestAttemptService:
    def __init__(
        self,
        attempt_repository: LRITestAttemptRepository,
        answer_repository: LRITestAttemptAnswerRepository,
        learner_service: LearnerService,
        test_service: LRITestService, 
    ):
        self._attempt_repository = attempt_repository
        self._answer_repository = answer_repository
        self._learner_service = learner_service
        self._test_service = test_service

    async def create(
        self,
        test_id: int,
        user_id: int,
        attempt_create: LRITestAttemptCreate,
    ) -> LRITestAttemptResponse:
        learner = await self._learner_service.get_by_user_id(user_id)
        test = await self._test_service.get_by_id(test_id)

        answers = attempt_create.answers
        test_with_items = await self._test_service.get_by_id_with_items(test_id)
        test_item_ids = {item.item_id for item in test_with_items.items}
        answer_item_ids = [answer.item_id for answer in answers]

        # Do not accept partial, duplicate, or cross-test submissions. The
        # score is only meaningful when each LRI statement has one response.
        if (
            len(answer_item_ids) != len(test_item_ids)
            or len(set(answer_item_ids)) != len(answer_item_ids)
            or set(answer_item_ids) != test_item_ids
        ):
            raise InvalidTestAttemptError()

        # Utilize accumulator pattern to get total score
        score_sum = 0

        for answer in answers:
            score_sum += answer.answer_value

        lri_score = score_sum / len(answers)

        attempt = await self._attempt_repository.create(
            LRITestAttempt(
                test_id=test.id,
                learner_id=learner.id,
                lri_score=lri_score,
            )
        )

        for answer in answers:
            answer = await self._answer_repository.create(
                LRITestAttemptAnswer(
                    attempt_id=attempt.id,
                    item_id=answer.item_id,
                    answer_value=answer.answer_value,
                )
            )

        return LRITestAttemptResponse(
            attempt_id=attempt.id,
            status="submitted",
        )

    async def get_result(self, user_id: int, test_id: int) -> LRITestAttemptResultResponse:
        """The calling learner's own attempt for a test, with its stored lri_score.

        The learner is always derived from the authenticated user and used as a
        filter, so another learner's attempt can never be returned.
        """
        learner = await self._learner_service.get_by_user_id(user_id)

        attempt = await self._attempt_repository.get_by_test_and_learner(
            test_id, learner.id
        )

        if attempt is None:
            raise LRITestAttemptNotFoundError()

        return LRITestAttemptResultResponse(
            attempt_id=attempt.id,
            test_id=attempt.test_id,
            lri_score=attempt.lri_score,
            submitted_at=attempt.submitted_at,
        )
