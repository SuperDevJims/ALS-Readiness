# This script seeds the LRI test along with its items.
# Scope: LRI test for Learner Readiness Index assessment.
# Run 'uv run python -m scripts.seed_lri_test'.

import asyncio
import sys

from sqlalchemy.ext.asyncio import AsyncSession

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from app.db.session import AsyncSessionLocal
from app.models.lri_test import LRITest, LRITestItem
from app.repositories.lri_test import LRITestRepository
from app.repositories.lri_test_item import LRITestItemRepository

LRI_TEST_DATA = {
    "title": "Learner Readiness Index Assessment",
    "description": (
        "An assessment used to measure the learner's readiness "
        "for learning and educational content."
    ),
    "image_url": "https://images.unsplash.com/photo-1457369804613-52c61a468e7d?auto=format&fit=crop&w=1200&q=80",
    "items": [
        "I can understand instructions given by my teacher.",
        "I can focus on a learning activity until I finish it.",
        "I feel confident when learning something new.",
        "I can remember important information from a lesson.",
        "I can follow a learning activity step by step.",
        "I can ask for help when I do not understand something.",
        "I can complete learning activities even when they are difficult.",
        "I can manage my time when completing school activities.",
        "I am willing to learn new topics and skills.",
        "I can stay motivated when working on a difficult activity.",
    ],
}


async def create_lri_test(session: AsyncSession) -> LRITest:
    test_repo = LRITestRepository(session)
    item_repo = LRITestItemRepository(session)

    test = await test_repo.create(
        LRITest(
            title=LRI_TEST_DATA["title"],
            description=LRI_TEST_DATA["description"],
        )
    )

    for question_text in LRI_TEST_DATA["items"]:
        _ = await item_repo.create(
            LRITestItem(
                test_id=test.id,
                question_text=question_text,
            )
        )

    print(f"LRI test created - id: {test.id}")

    return test


async def main() -> None:
    async with AsyncSessionLocal() as session, session.begin():
        await create_lri_test(session)


if __name__ == "__main__":
    asyncio.run(main())
