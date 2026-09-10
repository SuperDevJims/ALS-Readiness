import asyncio

from app.db.session import AsyncSessionLocal
from app.enums.user import UserRole
from app.models.facilitator import Facilitator
from app.models.user import User
from app.repositories.facilitator import FacilitatorRepository

from .seed_profile import create_profile
from .seed_user import create_user


async def create_facilitator(session) -> tuple[User, Facilitator]:
    facilitator_repo = FacilitatorRepository(session)

    user = await create_user(UserRole.FACILITATOR, session)
    _ = await create_profile(user.id, {"first_name": "Dennis", "last_name": "Martillano"}, session)


    facilitator = await facilitator_repo.create(
        Facilitator(
            user_id=user.id
        )
    )

    return user, facilitator


async def main():
    async with AsyncSessionLocal() as session, session.begin():
        await create_facilitator(session)


if __name__ == "__main__":
    asyncio.run(main())
