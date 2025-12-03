from fastapi import Depends

from app.core.unit_of_work import UnitOfWork
from app.modules.ads.services import AdService
from app.shared.dependencies import get_object_storage_service, get_unit_of_work
from app.shared.object_storage import ObjectStorageService


async def get_ad_service(
    uow: UnitOfWork = Depends(get_unit_of_work),
    object_storage_service: ObjectStorageService = Depends(get_object_storage_service),
) -> AdService:
    return AdService(uow, object_storage_service)
