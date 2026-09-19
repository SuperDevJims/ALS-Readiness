# This script seeds the learning strands (LS1-EN, LS1-FIL, LS3). There are no
# module or lesson tables to seed.
# Scope: LS1-EN, LS1-FIL, LS3 only, per thesis Delimitation.
# Run 'uv run python -m scripts.seed_learning_strand'.

import asyncio
import sys

from sqlalchemy.ext.asyncio import AsyncSession

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from app.db.session import AsyncSessionLocal
from app.models.learning_strand import LearningStrand
from app.repositories.learning_strand import LearningStrandRepository

CURRICULUM_DATA = {
    "LS1-EN": {
        "name": "Communication Skills (English)",
        "description": (
            "Covers listening, speaking, reading, and writing competencies "
            "in English, aligned with the ALS K-to-12 Basic Education Curriculum."
        )
    },
    "LS1-FIL": {
        "name": "Kasanayan sa Pakikipagtalastasan",
        "description": (
            "Sumasaklaw sa pakikinig, pagsasalita, pagbasa, at pagsulat "
            "gamit ang wikang Filipino, alinsunod sa ALS K to 12 Basic "
            "Education Curriculum."
        )
    },
    "LS3": {
        "name": "Mathematical and Problem Solving Skills",
        "description": (
            "Covers numeracy, logical reasoning, and problem-solving "
            "competencies aligned with the ALS K-to-12 Basic Education "
            "Curriculum."
        )
    }
}


async def create_strands(session: AsyncSession) -> None:
    strand_repo = LearningStrandRepository(session)

    for code, strand_data in CURRICULUM_DATA.items():
        strand = await strand_repo.create(
            LearningStrand(
                code=code,
                name=strand_data["name"],
                description=strand_data["description"],
            )
        )

        print(f"Strand created - code: {strand.code}, id: {strand.id}")



async def main() -> None:
    async with AsyncSessionLocal() as session, session.begin():
        await create_strands(session)


if __name__ == "__main__":
    asyncio.run(main())
