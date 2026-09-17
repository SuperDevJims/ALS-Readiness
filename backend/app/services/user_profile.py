from app.core.exceptions import UserProfileNotFoundError
from app.models.user_profile import UserProfile
from app.repositories.user_profile import UserProfileRepository
from app.schemas.user_profile import UserProfileCreate, UserProfileUpdate


class UserProfileService:
    def __init__(self, profile_repository: UserProfileRepository):
        self._profile_repository = profile_repository

    # ============ Public Methods ============

    async def create(self, user_id: int, profile_create: UserProfileCreate) -> UserProfile:
        return await self._profile_repository.create(
            UserProfile(
                user_id=user_id,
                **profile_create.model_dump(),
            )
        )

    async def get_by_user_id(self, user_id: int) -> UserProfile:
        profile = await self._profile_repository.get_by_user_id(user_id)

        if profile is None:
            raise UserProfileNotFoundError()

        return profile

    async def update(self, user_id: int, data: UserProfileUpdate) -> UserProfile:
        profile = await self.get_by_user_id(user_id)

        return await self._profile_repository.update(profile, data)
