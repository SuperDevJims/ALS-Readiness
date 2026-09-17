# This script seeds strand tests (pretest and posttest per strand),
# along with their items and item options.
# Scope: LS1-EN, LS1-FIL, LS3 only, per thesis Delimitation.
# Run 'uv run python -m scripts.seed_strand_test'.

import asyncio
import sys

from sqlalchemy.ext.asyncio import AsyncSession

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from app.db.session import AsyncSessionLocal
from app.models.strand_test import StrandTest, StrandTestItem, StrandTestItemOption
from app.repositories.learning_strand import LearningStrandRepository
from app.repositories.strand_test import StrandTestRepository
from app.repositories.strand_test_item import StrandTestItemRepository
from app.repositories.strand_test_item_option import StrandTestItemOptionRepository

# Each strand gets ONE pretest and ONE posttest.
# Each test has a small set of sample items, each item has options
# with exactly one marked is_correct=True.

STRAND_TEST_DATA = {
    "LS1-EN": {
        "pretest": {
            "title": "LS1-EN Diagnostic Pre-test",
            "image_url": "https://images.unsplash.com/photo-1455390582262-044cdead277a?auto=format&fit=crop&w=1200&q=80",
            "items": [
                (
                    "Which word is a pronoun?",
                    [("Run", False), ("She", True), ("Quickly", False), ("Table", False)],
                ),
                (
                    "Choose the correct verb tense: 'Yesterday, I ___ to the market.'",
                    [("go", False), ("goes", False), ("went", True), ("going", False)],
                ),
                (
                    "Which sentence is a compound sentence?",
                    [
                        ("I like rice.", False),
                        ("I like rice, but I also like bread.", True),
                        ("Rice and bread.", False),
                        ("Eating rice.", False),
                    ],
                ),
            ],
        },
        "posttest": {
            "title": "LS1-EN Post-test",
            "image_url": "https://images.unsplash.com/photo-1455390582262-044cdead277a?auto=format&fit=crop&w=1200&q=80",
            "items": [
                (
                    "Identify the noun in the sentence: 'The dog barked loudly.'",
                    [("dog", True), ("barked", False), ("loudly", False), ("the", False)],
                ),
                (
                    "What is the main idea of a paragraph usually found in?",
                    [
                        ("The topic sentence", True),
                        ("The last word", False),
                        ("A random sentence", False),
                        ("The title only", False),
                    ],
                ),
                (
                    "Choose the word closest in meaning to 'happy'.",
                    [("Sad", False), ("Joyful", True), ("Angry", False), ("Tired", False)],
                ),
            ],
        },
    },
    "LS1-FIL": {
        "pretest": {
            "title": "LS1-FIL Diagnostic Pre-test",
            "image_url": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=1200&q=80",
            "items": [
                (
                    "Alin sa mga sumusunod ang panghalip?",
                    [("Tumakbo", False), ("Siya", True), ("Mabilis", False), ("Mesa", False)],
                ),
                (
                    "Piliin ang tamang aspekto ng pandiwa: 'Kahapon, ___ ako sa palengke.'",
                    [("pumupunta", False), ("pupunta", False), ("pumunta", True), ("pagpunta", False)],
                ),
                (
                    "Alin sa mga sumusunod ang tambalang pangungusap?",
                    [
                        ("Mahilig ako sa kanin.", False),
                        ("Mahilig ako sa kanin, ngunit mahilig din ako sa tinapay.", True),
                        ("Kanin at tinapay.", False),
                        ("Kumakain ng kanin.", False),
                    ],
                ),
            ],
        },
        "posttest": {
            "title": "LS1-FIL Post-test",
            "image_url": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=1200&q=80",
            "items": [
                (
                    "Tukuyin ang pangngalan sa pangungusap: 'Tumahol nang malakas ang aso.'",
                    [("aso", True), ("tumahol", False), ("malakas", False), ("nang", False)],
                ),
                (
                    "Karaniwang matatagpuan saan ang pangunahing kaisipan ng talata?",
                    [
                        ("Sa paksang pangungusap", True),
                        ("Sa huling salita", False),
                        ("Sa random na pangungusap", False),
                        ("Sa pamagat lamang", False),
                    ],
                ),
                (
                    "Piliin ang salitang malapit sa kahulugan ng 'masaya'.",
                    [("Malungkot", False), ("Natutuwa", True), ("Galit", False), ("Pagod", False)],
                ),
            ],
        },
    },
    "LS3": {
        "pretest": {
            "title": "LS3 Diagnostic Pre-test",
            "image_url": "https://images.unsplash.com/photo-1509228468518-180dd4864904?auto=format&fit=crop&w=1200&q=80",
            "items": [
                (
                    "What is the value of the digit 5 in 5,432?",
                    [("5", False), ("50", False), ("500", False), ("5000", True)],
                ),
                (
                    "What is 245 + 178?",
                    [("423", True), ("413", False), ("433", False), ("323", False)],
                ),
                (
                    "What is 12 x 4?",
                    [("36", False), ("48", True), ("44", False), ("52", False)],
                ),
            ],
        },
        "posttest": {
            "title": "LS3 Post-test",
            "image_url": "https://images.unsplash.com/photo-1509228468518-180dd4864904?auto=format&fit=crop&w=1200&q=80",
            "items": [
                (
                    "What is 3/4 written as a decimal?",
                    [("0.34", False), ("0.75", True), ("0.43", False), ("1.34", False)],
                ),
                (
                    "Convert 0.5 to a fraction.",
                    [("1/5", False), ("1/2", True), ("5/10", False), ("2/5", False)],
                ),
                (
                    "A vendor sold 24 mangoes in the morning and 18 in the afternoon. How many mangoes were sold in total?",
                    [("42", True), ("36", False), ("40", False), ("32", False)],
                ),
            ],
        },
    },
}


async def create_strand_tests(session: AsyncSession) -> list[StrandTest]:
    strand_repo = LearningStrandRepository(session)
    test_repo = StrandTestRepository(session)
    item_repo = StrandTestItemRepository(session)
    option_repo = StrandTestItemOptionRepository(session)

    tests = [] 

    for code, test_types in STRAND_TEST_DATA.items():
        strand = await strand_repo.get_by_code(code)
        if not strand:
            print(f"Skipped - strand not found for code: {code}")
            continue

        for test_type, test_data in test_types.items():
            test = await test_repo.create(
                StrandTest(
                strand_id=strand.id,
                title=test_data["title"],
                image_url=test_data["image_url"],
                type=test_type,
                )
            )

            tests.append(test)
            print(f"Test created - code: {code}, type: {test_type}, id: {test.id}")

            for question_text, options in test_data["items"]:
                item = await item_repo.create(
                    StrandTestItem(
                        test_id=test.id,
                        question_text=question_text,
                    )
                )

                for option_text, is_correct in options:
                    _ = await option_repo.create(
                        StrandTestItemOption(
                            item_id=item.id,
                            option_text=option_text,
                            is_correct=is_correct,
                        )
                    )

    return tests


async def main() -> None:
    async with AsyncSessionLocal() as session, session.begin():
        await create_strand_tests(session)


if __name__ == "__main__":
    asyncio.run(main())
