from uuid import UUID

from fastapi import APIRouter, Depends

from app.modules.locations.dependencies import get_location_service
from app.modules.locations.schemas import LocationResponse
from app.modules.locations.services import LocationService
from app.shared.dependencies import get_accept_language, get_current_user

locations_router = APIRouter(prefix="/locations", tags=["Локации"])


@locations_router.get("/", response_model=list[LocationResponse])
async def get_locations(
    location_service: LocationService = Depends(get_location_service),
    accept_language: str = Depends(get_accept_language),
    _: UUID = Depends(get_current_user),
) -> list[LocationResponse]:
    return await location_service.get_locations(accept_language)
