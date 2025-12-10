from uuid import UUID

import aioboto3
from botocore.client import Config
from botocore.exceptions import ClientError

from app.shared.exceptions import (
    ObjectDeleteError,
    ObjectListGetError,
    ObjectUploadError,
)


class ObjectStorageService:
    AVATAR_KEY_PREFIX = "user_avatars/"
    AD_IMAGES_KEY_PREFIX = "ad_images/"

    def __init__(
        self,
        endpoint_url: str,
        access_key_id: str,
        secret_access_key: str,
        bucket_name: str,
    ):
        self.endpoint_url = endpoint_url
        self.bucket_name = bucket_name
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.session = aioboto3.Session()
        self.config = Config(signature_version="s3v4")

    async def _get_client(self):
        return self.session.client(
            "s3",
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key,
            config=self.config,
        )

    async def upload_avatar(self, user_id: UUID, file_data: bytes) -> str:
        try:
            key = f"{self.AVATAR_KEY_PREFIX}{user_id}.jpg"

            async with await self._get_client() as s3:
                await s3.put_object(
                    Bucket=self.bucket_name,
                    Key=key,
                    Body=file_data,
                    ContentType="image/jpeg",
                    Metadata={"user_id": str(user_id)},
                )

                return await self._generate_presigned_url(s3, key)
        except ClientError:
            raise ObjectUploadError(f"avatar {user_id}")

    async def delete_avatar(self, user_id: UUID) -> None:
        try:
            key = f"{self.AVATAR_KEY_PREFIX}{user_id}.jpg"
            async with await self._get_client() as s3:
                await s3.delete_object(Bucket=self.bucket_name, Key=key)
        except ClientError:
            raise ObjectDeleteError(f"avatar {user_id}")

    async def get_avatar_url(self, user_id: UUID) -> str | None:
        try:
            key = f"{self.AVATAR_KEY_PREFIX}{user_id}.jpg"
            async with await self._get_client() as s3:
                await s3.head_object(Bucket=self.bucket_name, Key=key)

                return await self._generate_presigned_url(s3, key)
        except ClientError:
            return None

    async def get_avatar_urls(self, user_ids: list[UUID]) -> dict[UUID, str | None]:
        try:
            keys = [f"{self.AVATAR_KEY_PREFIX}{user_id}.jpg" for user_id in user_ids]
            async with await self._get_client() as s3:
                response = await s3.list_objects_v2(
                    Bucket=self.bucket_name, Prefix=self.AVATAR_KEY_PREFIX
                )

                existing_keys = {obj["Key"] for obj in response.get("Contents", [])}
                result = {}

                for user_id, key in zip(user_ids, keys):
                    if key in existing_keys:
                        result[user_id] = await self._generate_presigned_url(s3, key)
                    else:
                        result[user_id] = None

                return result
        except ClientError:
            raise ObjectListGetError("avatar")

    async def avatar_exists(self, user_id: UUID) -> bool:
        try:
            key = f"{self.AVATAR_KEY_PREFIX}{user_id}.jpg"
            async with await self._get_client() as s3:
                await s3.head_object(Bucket=self.bucket_name, Key=key)

                return True
        except ClientError:
            return False

    async def upload_ad_images(
        self, ad_id: UUID, file_data_list: list[bytes]
    ) -> list[str]:
        try:
            keys = []
            async with await self._get_client() as s3:
                for index, file_data in enumerate(file_data_list):
                    key = f"{self.AD_IMAGES_KEY_PREFIX}{ad_id}/image_{index}.jpg"
                    await s3.put_object(
                        Bucket=self.bucket_name,
                        Key=key,
                        Body=file_data,
                        ContentType="image/jpeg",
                        Metadata={"ad_id": str(ad_id)},
                    )
                    keys.append(key)

                return [await self._generate_presigned_url(s3, key) for key in keys]
        except ClientError:
            raise ObjectUploadError(f"ad image {ad_id}")

    async def delete_ad_images(self, ad_id: UUID) -> None:
        try:
            keys = [
                f"{self.AD_IMAGES_KEY_PREFIX}{ad_id}/image_{index}.jpg"
                for index in range(10)
            ]
            async with await self._get_client() as s3:
                for key in keys:
                    await s3.delete_object(Bucket=self.bucket_name, Key=key)
        except ClientError:
            raise ObjectDeleteError(f"ad image {ad_id}")

    async def get_ad_images(self, ad_id: UUID) -> list[str]:
        try:
            async with await self._get_client() as s3:
                response = await s3.list_objects_v2(
                    Bucket=self.bucket_name,
                    Prefix=f"{self.AD_IMAGES_KEY_PREFIX}{ad_id}/",
                )

                existing_keys = [obj["Key"] for obj in response.get("Contents", [])]
                return [
                    await self._generate_presigned_url(s3, key) for key in existing_keys
                ]
        except ClientError:
            raise ObjectListGetError("ad images")

    async def _generate_presigned_url(
        self, s3_client, key: str, expires_in: int = 3600
    ) -> str:
        return await s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket_name, "Key": key},
            ExpiresIn=expires_in,
        )
