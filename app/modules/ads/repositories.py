from uuid import UUID

from sqlalchemy import String, and_, select

from app.modules.ads.models import Ad
from app.modules.categories.models import Category
from app.modules.locations.models import Location
from app.shared.repositories import Repository


class AdRepository(Repository):
    model = Ad

    async def find_all_with_details(
        self,
        accept_language: str,
        user_id: UUID | None = None,
        min_price: int | None = None,
        max_price: int | None = None,
        title: str | None = None,
        category_id: UUID | None = None,
        location_id: UUID | None = None,
    ) -> list[tuple[Ad, str, str]]:
        stmt = (
            select(
                Ad,
                Category.name_translations[accept_language].label("category_name"),
                Location.name_translations[accept_language].label("location_name"),
            )
            .join(Category, Ad.category_id == Category.id)
            .join(Location, Ad.location_id == Location.id)
        )

        conditions = []

        if user_id is not None:
            conditions.append(Ad.user_id == user_id)

        if min_price is not None:
            conditions.append(Ad.price >= min_price)

        if max_price is not None:
            conditions.append(Ad.price <= max_price)

        if title is not None:
            conditions.append(Ad.title.ilike(f"%{title}%"))

        if category_id is not None:
            conditions.append(Ad.category_id == category_id)

        if location_id is not None:
            conditions.append(Ad.location_id == location_id)

        if conditions:
            stmt = stmt.where(and_(*conditions))

        stmt = stmt.order_by(Ad.created_at.desc())

        result = await self.session.execute(stmt)
        return result.all()

    async def find_one_with_details(
        self, ad_id: UUID, accept_language: str
    ) -> tuple[Ad, str, str] | None:
        stmt = (
            select(
                Ad,
                Category.name_translations[accept_language].label("category_name"),
                Location.name_translations[accept_language].label("location_name"),
            )
            .join(Category, Ad.category_id == Category.id)
            .join(Location, Ad.location_id == Location.id)
            .where(Ad.id == ad_id)
        )

        result = await self.session.execute(stmt)
        return result.first()
