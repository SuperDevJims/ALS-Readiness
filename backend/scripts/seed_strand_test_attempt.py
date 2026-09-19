import asyncio
import sys
from random import randint
from typing import Any

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from app.db.session import AsyncSessionLocal
from app.repositories.learner import LearnerRepository
from app.repositories.strand_test import StrandTestRepository
from app.repositories.strand_test_attempt import StrandTestAttemptRepository
from app.repositories.strand_test_attempt_answers import (
    StrandTestAttemptAnswerRepository,
)
from app.repositories.strand_test_item_option import StrandTestItemOptionRepository
from app.schemas.strand_test_attempt import (
    StrandAttemptAnswerCreate,
    StrandAttemptCreate,
    StrandAttemptResponse,
)
from app.services.learner import LearnerService
from app.services.strand_test import StrandTestService
from app.services.strand_test_attempt import StrandTestAttemptService
from sqlalchemy.ext.asyncio import AsyncSession


async def create_strand_attempt(
    user_id: int,
    test_id: int,
    session: AsyncSession,
) -> StrandAttemptResponse:
    learner_repo = LearnerRepository(session)
    learner_service = LearnerService(learner_repo)

    test_repo = StrandTestRepository(session)
    test_service = StrandTestService(test_repo, learner_service)

    attempt_repo = StrandTestAttemptRepository(session)
    attempt_answer_repo = StrandTestAttemptAnswerRepository(session)
    item_option_repo = StrandTestItemOptionRepository(session)

    attempt_service = StrandTestAttemptService(
        attempt_repository=attempt_repo,
        attempt_answer_repository=attempt_answer_repo,
        test_option_repository=item_option_repo,
        test_repository=test_repo,
        learner_service=learner_service,
    )

    test_with_items = await test_service.get_by_id(test_id, True)
    items = test_with_items.items

    answers = []

    for item in items:
        options = [option for option in item.options]

        random_index = randint(0, len(options) - 1)

        chosen_option = options[random_index]

        answer = StrandAttemptAnswerCreate(
            item_id=item.item_id,
            option_id=chosen_option.option_id,
        )

        answers.append(answer)

    attempt_create = StrandAttemptCreate(answers=answers)
    attempt = await attempt_service.create(user_id, test_id, attempt_create)

    print(f"Strand test attempt created - id: {attempt.attempt_id}.")

    return attempt


async def main():
    async with AsyncSessionLocal() as session, session.begin():
        await create_strand_attempt(3, 13, session)


if __name__ == "__main__":
    asyncio.run(main())
