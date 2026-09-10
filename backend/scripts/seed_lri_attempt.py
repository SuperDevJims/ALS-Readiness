import asyncio
import sys
from random import randint

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from app.db.session import AsyncSessionLocal
from app.repositories.learner import LearnerRepository
from app.repositories.lri_test import LRITestRepository
from app.repositories.lri_test_attempt import LRITestAttemptRepository
from app.repositories.lri_test_attempt_answer import LRITestAttemptAnswerRepository
from app.schemas.lri_test_attempt import (
    LRITestAttemptAnswerCreate,
    LRITestAttemptCreate,
    LRITestAttemptResponse,
)
from app.services.learner import LearnerService
from app.services.lri_test import LRITestService
from app.services.lri_test_attempt import LRITestAttemptService
from sqlalchemy.ext.asyncio import AsyncSession


async def create_lri_attempt(
    user_id: int,
    test_id: int,
    session: AsyncSession,
) -> LRITestAttemptResponse:
    learner_repo = LearnerRepository(session)
    learner_service = LearnerService(learner_repo)

    lri_repo = LRITestRepository(session)
    lri_service = LRITestService(lri_repo, learner_service)

    attempt_repo = LRITestAttemptRepository(session)
    answer_repo_ = LRITestAttemptAnswerRepository(session)

    lri_attempt_service = LRITestAttemptService(attempt_repo, answer_repo_, learner_service, lri_service)

    lri_test = await lri_service.get_by_id_with_items(test_id)
    items = lri_test.items

    answers = []

    for item in items:
        random_answer = randint(1, 4)

        answers.append(
            LRITestAttemptAnswerCreate(
                answer_value=random_answer,
                item_id=item.item_id,
            )
        )

    attempt_create = LRITestAttemptCreate(answers=answers)
    attempt = await lri_attempt_service.create(test_id, user_id, attempt_create)

    print(f"LRI test attempt created - id {attempt.attempt_id}.")

    return 


async def main():
    async with AsyncSessionLocal() as session, session.begin():
        await create_lri_attempt(3, 3, session)


if __name__ == "__main__":
    asyncio.run(main())