from typing import Any
from uuid import UUID

from app.core.unit_of_work import UnitOfWork
from app.modules.ads.exceptions import AdNotFoundError, AdPermissionError
from app.modules.ads.schemas import AdCreate, AdResponse, AdUpdate
from app.modules.categories.exceptions import CategoryNotFoundError
from app.modules.categories.schemas import CategoryResponse
from app.modules.locations.exceptions import LocationNotFoundError
from app.modules.locations.schemas import LocationResponse
from app.shared.object_storage import ObjectStorageService


class AdService:
    def __init__(self, uow: UnitOfWork, object_storage: ObjectStorageService):
        self.uow = uow
        self.object_storage = object_storage

    async def get_ads(
        self,
        user_id: UUID,
        accept_language: str,
        filters: dict[str, Any] | None = None,
    ) -> list[AdResponse]:
        if filters is None:
            filters = {}

        min_price = filters.get("min_price")
        max_price = filters.get("max_price")
        title = filters.get("title")
        category_id = filters.get("category_id")
        location_id = filters.get("location_id")
        ad_ids = filters.get("ad_ids")

        async with self.uow as uow:
            rows = await uow.ad.find_all_with_details(
                min_price=min_price,
                max_price=max_price,
                title=title,
                category_id=category_id,
                location_id=location_id,
                accept_language=accept_language,
                ad_ids=ad_ids,
            )

            favorite_ids = set(await uow.favorite.get_favorite_ads_ids(user_id))

            ads_to_return = [
                AdResponse(
                    id=ad.id,
                    user_id=ad.user_id,
                    category=CategoryResponse(id=ad.category_id, name=category_name),
                    location=LocationResponse(id=ad.location_id, name=location_name),
                    price=ad.price,
                    title=ad.title,
                    description=ad.description,
                    images=await self.object_storage.get_ad_images(ad.id),
                    is_favorite=ad.id in favorite_ids,
                    created_at=ad.created_at,
                    updated_at=ad.updated_at,
                )
                for ad, category_name, location_name in rows
            ]

            return ads_to_return

    async def get_ad(
        self, ad_id: UUID, user_id: UUID, accept_language: str
    ) -> AdResponse:
        async with self.uow as uow:
            result = await uow.ad.find_one_with_details(ad_id, accept_language)

            if not result:
                raise AdNotFoundError(ad_id)

            ad, category_name, location_name = result

            if await uow.favorite.find_one(user_id=user_id, ad_id=ad_id):
                is_favorite = True
            else:
                is_favorite = False

            ad_to_return = AdResponse(
                id=ad.id,
                user_id=ad.user_id,
                category=CategoryResponse(id=ad.category_id, name=category_name),
                location=LocationResponse(id=ad.location_id, name=location_name),
                price=ad.price,
                title=ad.title,
                description=ad.description,
                images=await self.object_storage.get_ad_images(ad.id),
                is_favorite=is_favorite,
                created_at=ad.created_at,
                updated_at=ad.updated_at,
            )

            return ad_to_return

    async def create_ad(
        self, user_id: UUID, images_data: list[bytes], ad_create: AdCreate
    ) -> None:
        async with self.uow as uow:
            category = await uow.category.get_by_id(ad_create.category_id)
            if not category:
                raise CategoryNotFoundError(ad_create.category_id)

            location = await uow.location.get_by_id(ad_create.location_id)
            if not location:
                raise LocationNotFoundError(ad_create.location_id)

            ad_dict = ad_create.model_dump()
            ad_dict["user_id"] = user_id

            ad = await uow.ad.add_one(ad_dict)
            await uow.commit()

            await self.object_storage.upload_ad_images(ad.id, images_data)

    async def update_ad(
        self,
        ad_id: UUID,
        user_id: UUID,
        images_data: list[bytes] | None,
        ad_update: AdUpdate,
        accept_language: str,
    ) -> AdResponse:
        async with self.uow as uow:
            result = await uow.ad.find_one_with_details(ad_id, accept_language)

            if not result:
                raise AdNotFoundError(ad_id)

            ad, category_name, location_name = result

            if ad.user_id != user_id:
                raise AdPermissionError(ad_id)

            update_dict = ad_update.model_dump(exclude_unset=True, exclude_none=True)

            if "category_id" in update_dict:
                category = await uow.category.get_by_id(update_dict["category_id"])
                if not category:
                    raise CategoryNotFoundError(update_dict["category_id"])

            if "location_id" in update_dict:
                location = await uow.location.get_by_id(update_dict["location_id"])
                if not location:
                    raise LocationNotFoundError(update_dict["location_id"])

            updated_ad = await uow.ad.update(ad_id, update_dict)

            await uow.commit()

            if images_data is not None:
                await self.object_storage.upload_ad_images(ad.id, images_data)

            if await uow.favorite.find_one(user_id=user_id, ad_id=ad_id):
                is_favorite = True
            else:
                is_favorite = False

            ad_to_return = AdResponse(
                id=updated_ad.id,
                user_id=updated_ad.user_id,
                category=CategoryResponse(
                    id=updated_ad.category_id, name=category_name
                ),
                location=LocationResponse(
                    id=updated_ad.location_id, name=location_name
                ),
                price=updated_ad.price,
                title=updated_ad.title,
                description=updated_ad.description,
                images=await self.object_storage.get_ad_images(ad_id),
                is_favorite=is_favorite,
                created_at=updated_ad.created_at,
                updated_at=updated_ad.updated_at,
            )

            return ad_to_return

    async def delete_ad(self, ad_id: UUID, user_id: UUID) -> None:
        async with self.uow as uow:
            ad = await uow.ad.get_by_id(ad_id)

            if not ad:
                raise AdNotFoundError(ad_id)

            if ad.user_id != user_id:
                raise AdPermissionError(ad_id)

            await uow.ad.delete(ad_id)
            await uow.commit()

            await self.object_storage.delete_ad_images(ad_id)
