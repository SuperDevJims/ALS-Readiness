from typing import Any

from app.models.user_profile import UserProfile
from app.repositories.user_profile import UserProfileRepository
from sqlalchemy.ext.asyncio import AsyncSession


async def create_profile(user_id, data: dict[str, Any], session: AsyncSession) -> UserProfile:
    profile_repo = UserProfileRepository(session)

    profile = await profile_repo.create(
        UserProfile(
            user_id=user_id,
            **data
        )
    )

    return profile