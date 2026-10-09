# This script seeds the curriculum structure: learning strands, modules, and
# lessons for LS1-EN, LS1-FIL, LS3.
# Scope: LS1-EN, LS1-FIL, LS3 only, per thesis Delimitation.
# Run 'uv run python -m scripts.seed_curriculum'.

import asyncio
import sys

from sqlalchemy.ext.asyncio import AsyncSession

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from app.db.session import AsyncSessionLocal
from app.models.learning_strand import LearningStrand
from app.models.lesson import Lesson
from app.models.module import Module
from app.repositories.learning_strand import LearningStrandRepository
from app.repositories.lesson import LessonRepository
from app.repositories.module import ModuleRepository

CURRICULUM_DATA = {
    "LS1-EN": {
        "name": "Communication Skills (English)",
        "description": (
            "Covers listening, speaking, reading, and writing competencies "
            "in English, aligned with the ALS K-to-12 Basic Education Curriculum."
        ),
        "modules": [
            {
                "title": "Listening and Speaking Skills",
                "description": (
                    "Develops learners' ability to comprehend spoken English "
                    "and express ideas clearly in conversation."
                ),
                "lessons": [
                    {
                        "title": "Active Listening Strategies",
                        "description": (
                            "Introduces techniques for understanding spoken "
                            "instructions, conversations, and short talks."
                        ),
                    },
                    {
                        "title": "Everyday Conversations",
                        "description": (
                            "Practices common conversational exchanges used "
                            "in daily situations such as greetings and requests."
                        ),
                    },
                ],
            },
            {
                "title": "Reading and Writing Skills",
                "description": (
                    "Builds learners' ability to comprehend written texts and "
                    "produce clear, organized written work."
                ),
                "lessons": [
                    {
                        "title": "Reading Comprehension Basics",
                        "description": (
                            "Covers identifying main ideas, details, and "
                            "sequence in short passages."
                        ),
                    },
                    {
                        "title": "Writing Simple Paragraphs",
                        "description": (
                            "Guides learners in constructing paragraphs with "
                            "a clear topic sentence and supporting details."
                        ),
                    },
                ],
            },
        ],
    },
    "LS1-FIL": {
        "name": "Kasanayan sa Pakikipagtalastasan",
        "description": (
            "Sumasaklaw sa pakikinig, pagsasalita, pagbasa, at pagsulat "
            "gamit ang wikang Filipino, alinsunod sa ALS K to 12 Basic "
            "Education Curriculum."
        ),
        "modules": [
            {
                "title": "Kasanayan sa Pakikinig at Pagsasalita",
                "description": (
                    "Nagpapalawak ng kakayahang unawain ang mga sinasabi at "
                    "magpahayag ng ideya sa wikang Filipino."
                ),
                "lessons": [
                    {
                        "title": "Mga Estratehiya sa Mabisang Pakikinig",
                        "description": (
                            "Ipinapakilala ang mga paraan ng pag-unawa sa "
                            "mga panuto at usapan."
                        ),
                    },
                    {
                        "title": "Pang-araw-araw na Pakikipag-usap",
                        "description": (
                            "Nagsasanay sa karaniwang usapan tulad ng "
                            "pagbati at paghingi ng tulong."
                        ),
                    },
                ],
            },
            {
                "title": "Kasanayan sa Pagbasa at Pagsulat",
                "description": (
                    "Nagpapaunlad ng kakayahang unawain ang binasang teksto "
                    "at makasulat nang malinaw."
                ),
                "lessons": [
                    {
                        "title": "Pag-unawa sa Binasa",
                        "description": (
                            "Tumatalakay sa paghahanap ng pangunahing ideya "
                            "at detalye sa maikling teksto."
                        ),
                    },
                    {
                        "title": "Pagsulat ng Simpleng Talata",
                        "description": (
                            "Naggagabay sa mag-aaral sa paggawa ng talata na "
                            "may malinaw na paksang pangungusap."
                        ),
                    },
                ],
            },
        ],
    },
    "LS3": {
        "name": "Mathematical and Problem Solving Skills",
        "description": (
            "Covers numeracy, logical reasoning, and problem-solving "
            "competencies aligned with the ALS K-to-12 Basic Education "
            "Curriculum."
        ),
        "modules": [
            {
                "title": "Numbers and Operations",
                "description": (
                    "Develops fluency in basic arithmetic operations and "
                    "number sense."
                ),
                "lessons": [
                    {
                        "title": "Whole Numbers and Place Value",
                        "description": (
                            "Covers reading, writing, and comparing whole "
                            "numbers using place value concepts."
                        ),
                    },
                    {
                        "title": "Addition and Subtraction",
                        "description": (
                            "Practices solving problems involving addition "
                            "and subtraction of whole numbers."
                        ),
                    },
                ],
            },
            {
                "title": "Problem Solving and Reasoning",
                "description": (
                    "Builds logical reasoning skills through real-world "
                    "problem-solving tasks."
                ),
                "lessons": [
                    {
                        "title": "Word Problems in Daily Life",
                        "description": (
                            "Applies arithmetic skills to solve practical, "
                            "everyday word problems."
                        ),
                    },
                    {
                        "title": "Patterns and Logical Reasoning",
                        "description": (
                            "Introduces identifying and extending numerical "
                            "and visual patterns."
                        ),
                    },
                ],
            },
        ],
    },
}


async def create_strands_with_structure(session: AsyncSession) -> None:
    strand_repo = LearningStrandRepository(session)
    module_repo = ModuleRepository(session)
    lesson_repo = LessonRepository(session)

    for code, strand_data in CURRICULUM_DATA.items():
        strand = await strand_repo.create(
            LearningStrand(
                code=code,
                name=strand_data["name"],
                description=strand_data["description"],
            )
        )
        print(f"Strand created - code: {strand.code}, id: {strand.id}")

        for module_index, module_data in enumerate(strand_data["modules"], start=1):
            module = await module_repo.create(
                Module(
                    strand_id=strand.id,
                    title=module_data["title"],
                    description=module_data["description"],
                    order_index=module_index,
                )
            )
            print(f"  Module created - title: {module.title}, id: {module.id}")

            for lesson_index, lesson_data in enumerate(module_data["lessons"], start=1):
                lesson = await lesson_repo.create(
                    Lesson(
                        module_id=module.id,
                        title=lesson_data["title"],
                        description=lesson_data["description"],
                        order_index=lesson_index,
                    )
                )
                print(f"    Lesson created - title: {lesson.title}, id: {lesson.id}")


async def main() -> None:
    async with AsyncSessionLocal() as session, session.begin():
        await create_strands_with_structure(session)


if __name__ == "__main__":
    asyncio.run(main())