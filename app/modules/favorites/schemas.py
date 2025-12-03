from uuid import UUID

from pydantic import BaseModel, ConfigDict


class FavoriteBase(BaseModel):
    ad_id: UUID


class FavoriteCreate(FavoriteBase):
    pass


class FavoriteResponse(FavoriteBase):
    model_config = ConfigDict(from_attributes=True)

    user_id: UUID
