from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import JSONResponse

from app.modules.ads.dependencies import get_ad_service
from app.modules.ads.schemas import AdCreate, AdResponse, AdUpdate
from app.modules.ads.services import AdService
from app.shared.dependencies import get_accept_language, get_current_user

ads_router = APIRouter(prefix="/ads", tags=["Объявления"])


@ads_router.get("/{ad_id}", response_model=AdResponse)
async def get_ad(
    ad_id: UUID,
    ad_service: AdService = Depends(get_ad_service),
    accept_language: str = Depends(get_accept_language),
    _: UUID = Depends(get_current_user),
) -> AdResponse:
    return await ad_service.get_ad(ad_id, accept_language)


@ads_router.get("/", response_model=list[AdResponse])
async def get_ads(
    min_price: int | None = Query(None, ge=0, description="Минимальная цена"),
    max_price: int | None = Query(None, ge=0, description="Максимальная цена"),
    title: str | None = Query(
        None, min_length=1, max_length=200, description="Поиск по заголовку"
    ),
    category_id: UUID | None = Query(None, description="ID категории"),
    location_id: UUID | None = Query(None, description="ID локации"),
    my_ads: bool = Query(False, description="Получить только мои объявления"),
    ad_service: AdService = Depends(get_ad_service),
    accept_language: str = Depends(get_accept_language),
    user_id: UUID = Depends(get_current_user),
) -> list[AdResponse]:
    filters = {}

    if min_price is not None:
        filters["min_price"] = min_price
    if max_price is not None:
        filters["max_price"] = max_price
    if title:
        filters["title"] = title
    if category_id:
        filters["category_id"] = category_id
    if location_id:
        filters["location_id"] = location_id

    target_user_id = user_id if my_ads else None

    return await ad_service.get_ads(
        filters=filters, user_id=target_user_id, accept_language=accept_language
    )


@ads_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_ad(
    ad_create: AdCreate,
    ad_service: AdService = Depends(get_ad_service),
    user_id: UUID = Depends(get_current_user),
) -> JSONResponse:
    await ad_service.create_ad(user_id, ad_create)
    return {"detail": "Ad created successfully"}


@ads_router.patch("/{ad_id}", response_model=AdResponse)
async def update_ad(
    ad_id: UUID,
    ad_update: AdUpdate,
    ad_service: AdService = Depends(get_ad_service),
    accept_language: str = Depends(get_accept_language),
    user_id: UUID = Depends(get_current_user),
) -> AdResponse:
    return await ad_service.update_ad(
        ad_id=ad_id,
        user_id=user_id,
        ad_update=ad_update,
        accept_language=accept_language,
    )


@ads_router.delete("/{ad_id}")
async def delete_ad(
    ad_id: UUID,
    ad_service: AdService = Depends(get_ad_service),
    user_id: UUID = Depends(get_current_user),
) -> JSONResponse:
    await ad_service.delete_ad(ad_id, user_id)
    return {"detail": "Ad deleted successfully"}
