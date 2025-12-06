from uuid import UUID

from app.core.security import get_password_hash
from app.core.unit_of_work import UnitOfWork
from app.modules.users.exceptions import UserNotFoundError
from app.modules.users.schemas import (
    UserAvatarResponse,
    UserResponse,
    UserStatsResponse,
    UserUpdate,
)
from app.shared.exceptions import FileTooLargeError, UnsupportedMediaTypeError
from app.shared.object_storage import ObjectStorageService


class UserService:

    def __init__(self, uow: UnitOfWork, object_storage_service: ObjectStorageService):
        self.uow = uow
        self.object_storage_service = object_storage_service

    async def get_user(self, user_id: UUID) -> UserResponse:
        async with self.uow as uow:
            user = await uow.user.get_by_id(user_id)
            if not user:
                raise UserNotFoundError(user_id)

            user_to_return = UserResponse.model_validate(user)
            user_to_return.avatar_url = (
                await self.object_storage_service.get_avatar_url(user_id)
            )

            return user_to_return

    async def get_users(self) -> list[UserResponse]:
        async with self.uow as uow:
            users = await uow.user.find_all()
            user_ids = [user.id for user in users]
            avatar_urls = await self.object_storage_service.get_avatar_urls(user_ids)

            users_to_return = []
            for user in users:
                user_to_return = UserResponse.model_validate(user)
                user_to_return.avatar_url = avatar_urls.get(user.id)

                users_to_return.append(user_to_return)

            return users_to_return

    async def get_user_stats(self, user_id: UUID) -> UserStatsResponse:
        async with self.uow as uow:
            user = await uow.user.get_by_id(user_id)
            if not user:
                raise UserNotFoundError(user_id)

            active_ads_count = await uow.ad.count_user_ads(user_id)

            return UserStatsResponse(active_ads_count=active_ads_count)

    async def update_user(self, user_id: UUID, user_update: UserUpdate) -> UserResponse:
        user_dict = user_update.model_dump(exclude_unset=True, exclude_none=True)
        if "password" in user_dict:
            user_dict["password_hash"] = get_password_hash(user_dict.pop("password"))
        async with self.uow as uow:
            user = await uow.user.update(user_id, user_dict)
            if not user:
                raise UserNotFoundError(user_id)

            user_to_return = UserResponse.model_validate(user)
            user_to_return.avatar_url = (
                await self.object_storage_service.get_avatar_url(user_id)
            )

            await uow.commit()

            return user_to_return

    async def delete_user(self, user_id: UUID) -> None:
        async with self.uow as uow:
            user = await uow.user.get_by_id(user_id)
            if not user:
                raise UserNotFoundError(user_id)

            existing_avatar = await self.object_storage_service.avatar_exists(user_id)

            if existing_avatar:
                await self.object_storage_service.delete_avatar(user_id)

            user_ads = await uow.ad.find_all(user_id=user_id)
            for ad in user_ads:
                await self.object_storage_service.delete_ad_images(ad.id)

            await uow.user.delete(user_id)

            await uow.commit()

    async def upload_avatar(
        self, user_id: UUID, file_data: bytes, content_type: str
    ) -> UserAvatarResponse:
        async with self.uow as uow:
            user = await uow.user.get_by_id(user_id)
            if not user:
                raise UserNotFoundError(user_id)

            if not content_type.startswith("image/"):
                raise UnsupportedMediaTypeError("File must be an image")

            if len(file_data) > 5 * 1024 * 1024:
                raise FileTooLargeError("File is too large. Maximum size: 5MB")

            avatar_url = await self.object_storage_service.upload_avatar(
                user_id, file_data
            )

            avatar_to_return = UserAvatarResponse.model_validate(
                {"avatar_url": avatar_url}
            )

            return avatar_to_return

    async def delete_avatar(self, user_id: UUID) -> None:
        async with self.uow as uow:
            user = await uow.user.get_by_id(user_id)
            if not user:
                raise UserNotFoundError(user_id)

            await self.object_storage_service.delete_avatar(user_id)
