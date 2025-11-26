from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.modules.users.dependencies import get_user_service
from app.modules.users.schemas import UserCreate, UserResponse, UserUpdate
from app.modules.users.services import UserService

users_router = APIRouter(prefix="/users", tags=["Пользователи"])


@users_router.post(
    "/", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register(
    user_create: UserCreate, user_service: UserService = Depends(get_user_service)
) -> UserResponse:
    return await user_service.create_user(user_create)


@users_router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID,
    user_service: UserService = Depends(get_user_service),
) -> UserResponse:
    return await user_service.get_user(user_id)


@users_router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: UUID,
    user_update: UserUpdate,
    user_service: UserService = Depends(get_user_service),
) -> UserResponse:
    return await user_service.update_user(user_id, user_update)


@users_router.delete("/{user_id}")
async def delete_user(
    user_id: UUID,
    user_service: UserService = Depends(get_user_service),
) -> JSONResponse:
    await user_service.delete_user(user_id)
    return {"detail": "User deleted successfully"}
