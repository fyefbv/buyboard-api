from datetime import datetime
from uuid import UUID

from fastapi import Form
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

    @classmethod
    def as_form(
        cls,
        category_id: UUID = Form(),
        location_id: UUID = Form(),
        price: int = Form(),
        title: str = Form(),
        description: str | None = Form(None),
    ):
        return cls(
            category_id=category_id,
            location_id=location_id,
            price=price,
            title=title,
            description=description,
        )


class AdUpdate(AdBase):
    category_id: UUID | None = None
    location_id: UUID | None = None
    price: int | None = None
    title: str | None = None

    @classmethod
    def as_form(
        cls,
        category_id: UUID | None = Form(None),
        location_id: UUID | None = Form(None),
        price: int | None = Form(None),
        title: str | None = Form(None),
        description: str | None = Form(None),
    ):
        return cls(
            category_id=category_id,
            location_id=location_id,
            price=price,
            title=title,
            description=description,
        )


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
