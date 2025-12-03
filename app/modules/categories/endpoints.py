from uuid import UUID

from fastapi import APIRouter, Depends

from app.modules.categories.dependencies import get_category_service
from app.modules.categories.schemas import CategoryResponse
from app.modules.categories.services import CategoryService
from app.shared.dependencies import get_accept_language, get_current_user_id

categories_router = APIRouter(prefix="/categories", tags=["Категории"])


@categories_router.get("/", response_model=list[CategoryResponse])
async def get_categories(
    category_service: CategoryService = Depends(get_category_service),
    accept_language: str = Depends(get_accept_language),
    _: UUID = Depends(get_current_user_id),
) -> list[CategoryResponse]:
    return await category_service.get_categories(accept_language)
