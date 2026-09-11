from app.core.exceptions import LRITestNotFoundError
from app.models.lri_test_attempt import LRITestAttempt, LRITestAttemptAnswer
from app.repositories.lri_test_attempt import LRITestAttemptRepository
from app.repositories.lri_test_attempt_answer import LRITestAttemptAnswerRepository
from app.schemas.lri_test_attempt import LRITestAttemptCreate, LRITestAttemptResponse

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
