from fastapi import Depends

from app.core.unit_of_work import UnitOfWork
from app.modules.ads.services import AdService
from app.shared.dependencies import get_unit_of_work


async def get_ad_service(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> AdService:
    return AdService(uow)
