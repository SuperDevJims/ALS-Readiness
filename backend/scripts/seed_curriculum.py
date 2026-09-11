# This script seeds the curriculum structure (learning strands, modules, lessons).
# Scope: LS1-EN, LS1-FIL, LS3 only, per thesis Delimitation.
# Run 'uv run python -m scripts.seed_curriculum'.

import asyncio
import sys

from sqlalchemy.ext.asyncio import AsyncSession

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from app.db.session import AsyncSessionLocal
from app.models.curriculum import LearningStrand, Lesson, Module
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
            (
                "Basic Grammar and Sentence Structure",
                [
                    "Nouns and Pronouns",
                    "Verb Tenses",
                    "Building Simple and Compound Sentences",
                ],
            ),
            (
                "Reading Comprehension and Vocabulary",
                [
                    "Identifying Main Idea and Details",
                    "Context Clues and Vocabulary Building",
                    "Reading Short Passages for Comprehension",
                ],
            ),
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
            (
                "Gramatika at Pang-unawa sa Pangungusap",
                [
                    "Pangngalan at Panghalip",
                    "Aspekto ng Pandiwa",
                    "Paggawa ng Simple at Tambalang Pangungusap",
                ],
            ),
            (
                "Pag-unawa sa Binasa at Talasalitaan",
                [
                    "Pagtukoy sa Pangunahing Kaisipan",
                    "Paggamit ng Konteksto sa Bagong Salita",
                    "Pagbasa ng Maiikling Sipi",
                ],
            ),
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
            (
                "Whole Numbers and Basic Operations",
                [
                    "Place Value and Number Sense",
                    "Addition and Subtraction of Whole Numbers",
                    "Multiplication and Division of Whole Numbers",
                ],
            ),
            (
                "Fractions, Decimals, and Problem Solving",
                [
                    "Introduction to Fractions",
                    "Converting Fractions and Decimals",
                    "Solving Word Problems with Basic Operations",
                ],
            ),
        ],
    },
}


async def create_curriculum(session: AsyncSession) -> None:
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

        for module_order, (module_name, lesson_names) in enumerate(
            strand_data["modules"], start=1
        ):
            module = await module_repo.create(
                Module(
                    strand_id=strand.id,
                    name=module_name,
                    order_index=module_order,
                )
            )
            print(f"  Module created - name: {module.name}, id: {module.id}")

            for lesson_order, lesson_name in enumerate(lesson_names, start=1):
                lesson = await lesson_repo.create(
                    Lesson(
                        module_id=module.id,
                        name=lesson_name,
                        order_index=lesson_order,
                    )
                )
                print(f"    Lesson created - name: {lesson.name}, id: {lesson.id}")


async def main() -> None:
    async with AsyncSessionLocal() as session, session.begin():
        await create_curriculum(session)


if __name__ == "__main__":
    asyncio.run(main())
