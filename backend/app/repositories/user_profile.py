from app.models.user_profile import UserProfile
from app.schemas.user_profile import UserProfileUpdate

from .base import BaseRepository


class UserProfileRepository(BaseRepository[UserProfile]):

    model = UserProfile

    async def update(
        self,
        user_profile: UserProfile,
        data: UserProfileUpdate,
    ) -> UserProfile:
        user_profile.sqlmodel_update(
            data.model_dump(exclude_unset=True)
        )
        
        await self._session.flush()
        await self._session.refresh(user_profile)
        
        return user_profile

    async def get_by_user_id(self, user_id: int) -> UserProfile | None:
        return await self._session.get(UserProfile, user_id)
