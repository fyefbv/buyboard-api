from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.modules.users.dependencies import get_user_service
from app.modules.users.schemas import UserResponse, UserUpdate
from app.modules.users.services import UserService
from app.shared.dependencies import get_current_user

users_router = APIRouter(prefix="/users", tags=["Пользователи"])


@users_router.get("/me", response_model=UserResponse)
async def get_user(
    user_service: UserService = Depends(get_user_service),
    user_id: UUID = Depends(get_current_user),
) -> UserResponse:
    return await user_service.get_user(user_id)


@users_router.patch("/me", response_model=UserResponse)
async def update_user(
    user_update: UserUpdate,
    user_service: UserService = Depends(get_user_service),
    user_id: UUID = Depends(get_current_user),
) -> UserResponse:
    return await user_service.update_user(user_id, user_update)


@users_router.delete("/me")
async def delete_user(
    user_service: UserService = Depends(get_user_service),
    user_id: UUID = Depends(get_current_user),
) -> JSONResponse:
    await user_service.delete_user(user_id)
    return {"detail": "User deleted successfully"}
