from app.core.unit_of_work import UnitOfWork
from app.modules.categories.schemas import CategoryResponse


class CategoryService:

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def get_categories(self, accept_language: str) -> list[CategoryResponse]:
        async with self.uow as uow:
            categories = await uow.category.find_all_with_localization(accept_language)
            categories_to_return = [
                CategoryResponse(
                    id=category.id, name=category.name_translations[accept_language]
                )
                for category in categories
            ]

            return categories_to_return
