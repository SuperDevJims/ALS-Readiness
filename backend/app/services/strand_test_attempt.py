from app.core.exceptions import InvalidTestAttemptError, StrandTestItemOptionNotFoundError
from app.models.strand_test_attempt import StrandTestAttempt, StrandTestAttemptAnswer
from app.repositories.strand_test_attempt import StrandTestAttemptRepository
from app.repositories.strand_test_attempt_answers import (
    StrandTestAttemptAnswerRepository,
)
from app.repositories.strand_test_item_option import StrandTestItemOptionRepository
from app.schemas.strand_test_attempt import StrandAttemptCreate, StrandAttemptResponse
from app.services.learner import LearnerService


class StrandTestAttemptService:
    def __init__(
        self,
        attempt_repository: StrandTestAttemptRepository,
        attempt_answer_repository: StrandTestAttemptAnswerRepository,
        test_option_repository:  StrandTestItemOptionRepository,
        learner_service: LearnerService,
    ):
        self._attempt_repository = attempt_repository
        self._attempt_answer_repository = attempt_answer_repository
        self._learner_service = learner_service
        self._test_option_repository = test_option_repository

    async def create(
        self,
        user_id: int,
        test_id: int,
        attempt_create: StrandAttemptCreate,
    ) -> StrandAttemptResponse:
        learner = await self._learner_service.get_by_user_id(user_id)
     
        test_options = await self._test_option_repository.get_by_test(test_id)

        # Turn test options into dictionaries for more efficient data access
        test_options_by_id = {
            opt.id: opt
            for opt in test_options
        }

        answers = attempt_create.answers

        # An answer is valid only when its option belongs to the supplied item,
        # and every item in this test is answered exactly once.
        test_item_ids = {option.item_id for option in test_options}
        answer_item_ids = [answer.item_id for answer in answers]
        if (
            len(answer_item_ids) != len(test_item_ids)
            or len(set(answer_item_ids)) != len(answer_item_ids)
            or set(answer_item_ids) != test_item_ids
        ):
            raise InvalidTestAttemptError()

        total_score = 0

        for answer in answers:
            option = test_options_by_id.get(answer.option_id)

            if option is None or option.item_id != answer.item_id:
                raise StrandTestItemOptionNotFoundError()

            if option.is_correct:
                total_score += 1

        # Store attempt in strand_test_attempts table
        attempt = await self._attempt_repository.create(
            StrandTestAttempt(
                test_id=test_id,
                learner_id=learner.id,
                total_score=total_score,
            )
        )

        # Store each answer in strand_test_attempt_answers table
        for answer in answers:
            option = test_options_by_id.get(answer.option_id)

            await self._attempt_answer_repository.create(
                StrandTestAttemptAnswer(
                    attempt_id=attempt.id,
                    item_id=answer.item_id,
                    option_id=answer.option_id,
                    is_correct=option.is_correct
                )
            )

        return StrandAttemptResponse(attempt_id=attempt.id, status="completed")        
