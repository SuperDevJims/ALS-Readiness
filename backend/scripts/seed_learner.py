import asyncio

from app.db.session import AsyncSessionLocal
from app.enums.user import UserRole
from app.models.learner import Learner
from app.models.user import User
from app.repositories.learner import LearnerRepository

from .seed_profile import create_profile
from .seed_user import create_user


async def create_learner(session) -> tuple[User, Learner]:
    learner_repo = LearnerRepository(session)

    user = await create_user(UserRole.LEARNER, session)
    _ = await create_profile(user.id, {"first_name": "Alternative", "middle_name": "Learning", "last_name": "System"}, session)


    learner = await learner_repo.create(
        Learner(
            user_id=user.id
        )
    )

    return user, learner


async def main():
    async with AsyncSessionLocal() as session, session.begin():
        await create_learner(session)


if __name__ == "__main__":
    asyncio.run(main())
