from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    login: str


class UserCreate(UserBase):
    email: EmailStr
    password: str


class UserLogin(UserBase):
    password: str


class UserUpdate(BaseModel):
    login: str | None = None
    email: EmailStr | None = None
    password: str | None = None


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: EmailStr
    avatar_url: str | None = None
    created_at: datetime
    updated_at: datetime
