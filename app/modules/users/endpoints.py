from uuid import UUID

from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import JSONResponse

from app.modules.users.dependencies import get_user_service
from app.modules.users.schemas import UserAvatarResponse, UserResponse, UserUpdate
from app.modules.users.services import UserService
from app.shared.dependencies import get_current_user_id

users_router = APIRouter(prefix="/users", tags=["Пользователи"])


@users_router.get("/{user_id}/", response_model=UserResponse)
async def get_user(
    user_id: UUID,
    user_service: UserService = Depends(get_user_service),
    _: UUID = Depends(get_current_user_id),
) -> UserResponse:
    return await user_service.get_user(user_id)


@users_router.get("/me", response_model=UserResponse)
async def get_current_user(
    user_service: UserService = Depends(get_user_service),
    user_id: UUID = Depends(get_current_user_id),
) -> UserResponse:
    return await user_service.get_user(user_id)


@users_router.patch("/me", response_model=UserResponse)
async def update_user(
    user_update: UserUpdate,
    user_service: UserService = Depends(get_user_service),
    user_id: UUID = Depends(get_current_user_id),
) -> UserResponse:
    return await user_service.update_user(user_id, user_update)


@users_router.delete("/me")
async def delete_user(
    user_service: UserService = Depends(get_user_service),
    user_id: UUID = Depends(get_current_user_id),
) -> JSONResponse:
    await user_service.delete_user(user_id)
    return {"detail": "User deleted successfully"}


@users_router.post("/me/avatar", response_model=UserAvatarResponse)
async def upload_avatar(
    file: UploadFile = File(),
    user_service: UserService = Depends(get_user_service),
    user_id: UUID = Depends(get_current_user_id),
) -> UserAvatarResponse:
    file_data = await file.read()

    return await user_service.upload_avatar(
        user_id,
        file_data,
        file.content_type,
    )


@users_router.delete("/me/avatar")
async def delete_avatar(
    user_service: UserService = Depends(get_user_service),
    user_id: UUID = Depends(get_current_user_id),
) -> JSONResponse:
    await user_service.delete_avatar(user_id)
    return {"detail": "User avatar deleted successfully"}
