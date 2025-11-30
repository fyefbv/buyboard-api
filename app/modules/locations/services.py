from app.core.unit_of_work import UnitOfWork
from app.modules.locations.schemas import LocationResponse


class LocationService:

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def get_locations(self, accept_language: str) -> list[LocationResponse]:
        async with self.uow as uow:
            locations = await uow.location.find_all_with_localization(accept_language)
            locations_to_return = [
                LocationResponse(
                    id=location.id, name=location.name_translations[accept_language]
                )
                for location in locations
            ]

            return locations_to_return
