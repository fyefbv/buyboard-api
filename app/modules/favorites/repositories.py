from typing import List
from uuid import UUID

from sqlalchemy import delete, select

from app.modules.favorites.models import Favorite
from app.shared.repositories import Repository


class FavoriteRepository(Repository):

    model = Favorite

    async def remove_from_favorites(self, user_id: UUID, ad_id: UUID) -> bool:
        stmt = delete(Favorite).where(
            Favorite.user_id == user_id, Favorite.ad_id == ad_id
        )
        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.rowcount > 0

    async def get_favorite_ads_ids(self, user_id: UUID) -> List[UUID]:
        stmt = select(Favorite.ad_id).where(Favorite.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()
