from uuid import UUID

import boto3
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
        self.s3 = boto3.client(
            "s3",
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            config=Config(signature_version="s3v4"),
        )

    async def upload_avatar(self, user_id: UUID, file_data: bytes) -> str:
        try:
            key = f"{self.AVATAR_KEY_PREFIX}{user_id}.jpg"

            self.s3.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=file_data,
                ContentType="image/jpeg",
                Metadata={"user_id": str(user_id)},
            )

            return self._generate_presigned_url(key)
        except ClientError as e:
            raise ObjectUploadError(f"avatar {user_id}")

    async def delete_avatar(self, user_id: UUID) -> None:
        try:
            key = f"{self.AVATAR_KEY_PREFIX}{user_id}.jpg"
            self.s3.delete_object(Bucket=self.bucket_name, Key=key)
        except ClientError as e:
            raise ObjectDeleteError(f"avatar {user_id}")

    async def get_avatar_url(self, user_id: UUID) -> str | None:
        try:
            key = f"{self.AVATAR_KEY_PREFIX}{user_id}.jpg"
            self.s3.head_object(Bucket=self.bucket_name, Key=key)

            return self._generate_presigned_url(key)
        except ClientError as e:
            return None

    async def avatar_exists(self, user_id: UUID) -> bool:
        try:
            key = f"{self.AVATAR_KEY_PREFIX}{user_id}.jpg"
            self.s3.head_object(Bucket=self.bucket_name, Key=key)

            return True
        except ClientError as e:
            return False

    async def upload_ad_images(
        self, ad_id: UUID, file_data_list: list[bytes]
    ) -> list[str]:
        try:
            keys = []
            for index, file_data in enumerate(file_data_list):
                key = f"{self.AD_IMAGES_KEY_PREFIX}{ad_id}/image_{index}.jpg"
                self.s3.put_object(
                    Bucket=self.bucket_name,
                    Key=key,
                    Body=file_data,
                    ContentType="image/jpeg",
                    Metadata={"ad_id": str(ad_id)},
                )
                keys.append(key)
            return [self._generate_presigned_url(key) for key in keys]
        except ClientError as e:
            raise ObjectUploadError(f"ad image {ad_id}")

    async def delete_ad_images(self, ad_id: UUID) -> None:
        try:
            keys = [
                f"{self.AD_IMAGES_KEY_PREFIX}{ad_id}/image_{index}.jpg"
                for index in range(10)
            ]
            for key in keys:
                self.s3.delete_object(Bucket=self.bucket_name, Key=key)
        except ClientError as e:
            raise ObjectDeleteError(f"ad image {ad_id}")

    async def get_ad_images(self, ad_id: UUID) -> list[str]:
        try:
            response = self.s3.list_objects_v2(
                Bucket=self.bucket_name, Prefix=f"{self.AD_IMAGES_KEY_PREFIX}{ad_id}/"
            )

            existing_keys = [obj["Key"] for obj in response.get("Contents", [])]
            return [self._generate_presigned_url(key) for key in existing_keys]
        except ClientError as e:
            raise ObjectListGetError("ad images")

    def _generate_presigned_url(self, key: str, expires_in: int = 3600) -> str:
        return self.s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket_name, "Key": key},
            ExpiresIn=expires_in,
        )
