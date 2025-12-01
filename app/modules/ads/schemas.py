from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.modules.categories.schemas import CategoryResponse
from app.modules.locations.schemas import LocationResponse


class AdBase(BaseModel):
    description: str | None = None


class AdCreate(AdBase):
    category_id: UUID
    location_id: UUID
    price: int
    title: str


class AdUpdate(AdBase):
    category_id: UUID | None = None
    location_id: UUID | None = None
    price: int | None = None
    title: str | None = None


class AdResponse(AdBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    category: CategoryResponse
    location: LocationResponse
    price: int
    title: str
    images: list[str]
    created_at: datetime
    updated_at: datetime
