from fastapi import Depends

from app.core.unit_of_work import UnitOfWork
from app.modules.users.services import UserService
from app.shared.dependencies import get_object_storage_service, get_unit_of_work
from app.shared.object_storage import ObjectStorageService


async def get_user_service(
    uow: UnitOfWork = Depends(get_unit_of_work),
    object_storage_service: ObjectStorageService = Depends(get_object_storage_service),
) -> UserService:
    return UserService(uow, object_storage_service)
