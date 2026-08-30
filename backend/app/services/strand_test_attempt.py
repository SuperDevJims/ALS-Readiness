from app.models.strand_test_attempt import StrandTestAttempt
from app.repositories.learner import LearnerRepository
from app.repositories.strand_test_attempt import StrandTestAttemptRepository
from app.repositories.strand_test_attempt_answers import (
    StrandTestAttemptAnswerRepository,
)
from app.repositories.strand_test_item_option import StrandTestItemOptionRepository
from app.schemas.strand_test_attempt import StrandAttemptCreate, StrandAttemptResponse


class StrandTestAttemptService:
    def __init__(
        self,
        attempt_repository: StrandTestAttemptRepository,
        attempt_answer_repository: StrandTestAttemptAnswerRepository,
        test_option_repository:  StrandTestItemOptionRepository,
        learner_repository: LearnerRepository,
    ):
        self._attempt_repository = attempt_repository
        self._attempt_answer_repository = attempt_answer_repository
        self._learner_repository = learner_repository
        self._test_option_repository = test_option_repository

    async def create(
        self,
        user_id: int,
        test_id: int,
        attempt_create: StrandAttemptCreate,
    ) -> StrandTestAttemptRepository:
        learner = self._learner_repository.get_by_user_id(user_id)
        
        answers = attempt_create.answers
        test_options = self._test_option_repository.get_by_test(test_id)

        print("Answers:", answers)
        print("Options in db:", test_options)


        # Calculate total score for the attempt 

        total = 0

        for answer in answers:
            pass

        """
        attempt = StrandTestAttempt(
            test_id=test_id,
            learner_id=learner.id,
        )
        """