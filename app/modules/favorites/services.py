from typing import List
from uuid import UUID

from app.core.unit_of_work import UnitOfWork
from app.modules.ads.exceptions import AdNotFoundError
from app.modules.ads.schemas import AdResponse
from app.modules.categories.schemas import CategoryResponse
from app.modules.favorites.exceptions import (
    CannotFavoriteOwnAdError,
    FavoriteAlreadyExistsError,
    FavoriteNotFoundError,
)
from app.modules.favorites.schemas import FavoriteResponse
from app.modules.locations.schemas import LocationResponse
from app.shared.object_storage import ObjectStorageService


class FavoriteService:
    def __init__(self, uow: UnitOfWork, object_storage: ObjectStorageService):
        self.uow = uow
        self.object_storage = object_storage

    async def get_favorites(
        self, user_id: UUID, accept_language: str
    ) -> List[AdResponse]:
        async with self.uow as uow:
            favorite_ads_ids = await uow.favorite.get_favorite_ads_ids(user_id)

            if not favorite_ads_ids:
                return []

            rows = await uow.ad.find_all_with_details(
                accept_language=accept_language,
                ad_ids=favorite_ads_ids,
            )

            return [
                AdResponse(
                    id=ad.id,
                    user_id=ad.user_id,
                    category=CategoryResponse(id=ad.category_id, name=category_name),
                    location=LocationResponse(id=ad.location_id, name=location_name),
                    price=ad.price,
                    title=ad.title,
                    description=ad.description,
                    images=await self.object_storage.get_ad_images(ad.id),
                    is_favorite=ad.id in favorite_ads_ids,
                    created_at=ad.created_at,
                    updated_at=ad.updated_at,
                )
                for ad, category_name, location_name in rows
            ]

    async def add_to_favorites(self, user_id: UUID, ad_id: UUID) -> FavoriteResponse:
        async with self.uow as uow:
            ad = await uow.ad.get_by_id(ad_id)
            if not ad:
                raise AdNotFoundError(ad_id)

            if ad.user_id == user_id:
                raise CannotFavoriteOwnAdError()

            if await uow.favorite.find_one(user_id=user_id, ad_id=ad_id):
                raise FavoriteAlreadyExistsError(f"user_id={user_id}, ad_id={ad_id}")

            favorite = await uow.favorite.add_one({"user_id": user_id, "ad_id": ad_id})
            await uow.commit()

            return FavoriteResponse(user_id=favorite.user_id, ad_id=favorite.ad_id)

    async def remove_from_favorites(self, user_id: UUID, ad_id: UUID) -> None:
        async with self.uow as uow:
            ad = await uow.ad.get_by_id(ad_id)

            if not ad:
                raise AdNotFoundError(ad_id)

            removed = await uow.favorite.remove_from_favorites(user_id, ad_id)
            if not removed:
                raise FavoriteNotFoundError(f"user_id={user_id}, ad_id={ad_id}")

            await uow.commit()
