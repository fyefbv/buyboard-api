from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.modules.ads.schemas import AdResponse
from app.modules.favorites.dependencies import get_favorite_service
from app.modules.favorites.schemas import FavoriteResponse
from app.modules.favorites.services import FavoriteService
from app.shared.dependencies import get_accept_language, get_current_user_id

favorites_router = APIRouter(prefix="/favorites", tags=["Избранное"])


@favorites_router.get("/", response_model=list[AdResponse])
async def get_favorites(
    accept_language: str = Depends(get_accept_language),
    favorite_service: FavoriteService = Depends(get_favorite_service),
    user_id: UUID = Depends(get_current_user_id),
) -> list[AdResponse]:
    return await favorite_service.get_favorites(user_id, accept_language)


@favorites_router.post("/{ad_id}", response_model=FavoriteResponse)
async def add_to_favorites(
    ad_id: UUID,
    favorite_service: FavoriteService = Depends(get_favorite_service),
    user_id: UUID = Depends(get_current_user_id),
) -> FavoriteResponse:
    return await favorite_service.add_to_favorites(user_id, ad_id)


@favorites_router.delete("/{ad_id}")
async def remove_from_favorites(
    ad_id: UUID,
    favorite_service: FavoriteService = Depends(get_favorite_service),
    user_id: UUID = Depends(get_current_user_id),
) -> JSONResponse:
    await favorite_service.remove_from_favorites(user_id, ad_id)
    return {"detail": "Ad removed from favorites successfully"}
