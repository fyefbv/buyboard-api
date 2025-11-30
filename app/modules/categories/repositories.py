from sqlalchemy import select

from app.modules.categories.models import Category
from app.shared.repositories import Repository


class CategoryRepository(Repository):

    model = Category

    async def find_all_with_localization(self, accept_language: str) -> list[Category]:
        stmt = select(self.model).where(
            self.model.name_translations[accept_language].astext.is_not(None)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
