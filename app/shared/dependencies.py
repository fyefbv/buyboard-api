from uuid import UUID

from fastapi import Depends, Header

from app.core.config import settings
from app.core.unit_of_work import UnitOfWork
from app.modules.auth.auth import decode_jwt, oauth2_scheme
from app.modules.auth.exceptions import MissingTokenError
from app.shared.object_storage import ObjectStorageService


async def get_unit_of_work() -> UnitOfWork:
    return UnitOfWork()


async def get_object_storage_service() -> ObjectStorageService:
    return ObjectStorageService(
        endpoint_url=settings.S3_ENDPOINT_URL,
        access_key_id=settings.S3_ACCESS_KEY_ID,
        secret_access_key=settings.S3_SECRET_ACCESS_KEY,
        bucket_name=settings.S3_BUCKET_NAME,
    )


async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> UUID:
    if not token:
        raise MissingTokenError()

    payload = decode_jwt(token)
    return UUID(payload.get("sub"))


async def get_accept_language(accept_language: str = Header(default="en")):
    return accept_language
