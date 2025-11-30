from fastapi import Depends

from app.core.unit_of_work import UnitOfWork
from app.modules.locations.services import LocationService
from app.shared.dependencies import get_unit_of_work


async def get_location_service(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> LocationService:
    return LocationService(uow)
