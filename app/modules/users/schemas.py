from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class UserUpdate(BaseModel):
    login: str | None = None
    email: EmailStr | None = None
    password: str | None = None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    login: str
    email: EmailStr
    avatar_url: str | None = None
    created_at: datetime
    updated_at: datetime


class UserAvatarResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    avatar_url: str | None = None


class UserStatsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    active_ads_count: int
