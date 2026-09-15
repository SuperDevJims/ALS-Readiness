from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.enums.user import UserRole
from app.schemas.user_profile import UserProfileResponse


class UserCreate(BaseModel):
    role: UserRole | None = Field(default=UserRole.LEARNER)


class UserPasswordUpdate(BaseModel):
    password: str = Field(min_length=8, max_length=128)


class UserResponse(BaseModel):
    id: int
    id_no: str
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserMeResponse(UserResponse):
    profile: UserProfileResponse


class PasswordChangeRequest(BaseModel):
    current_password: str = Field(min_length=1, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)
