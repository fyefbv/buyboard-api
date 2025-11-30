from sqlalchemy import select

from app.modules.locations.models import Location
from app.shared.repositories import Repository


class LocationRepository(Repository):

    model = Location

    async def find_all_with_localization(self, accept_language: str) -> list[Location]:
        stmt = select(self.model).where(
            self.model.name_translations[accept_language].astext.is_not(None)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
