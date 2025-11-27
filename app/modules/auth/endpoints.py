from fastapi import APIRouter, Depends, status

from app.modules.auth.auth import refresh_tokens
from app.modules.auth.dependencies import get_auth_service
from app.modules.auth.schemas import (
    TokenRefresh,
    TokenResponse,
    UserLogin,
    UserRegister,
)
from app.modules.auth.services import AuthService

auth_router = APIRouter(prefix="/auth", tags=["Аутентификация"])


@auth_router.post(
    "/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED
)
async def register(
    user_register: UserRegister, auth_service: AuthService = Depends(get_auth_service)
) -> TokenResponse:
    return await auth_service.register_user(user_register)


@auth_router.post("/login", response_model=TokenResponse)
async def login(
    user_login: UserLogin, auth_service: AuthService = Depends(get_auth_service)
) -> TokenResponse:
    return await auth_service.authenticate_user(user_login)


@auth_router.post("/refresh", response_model=TokenResponse)
async def refresh(refresh_token: TokenRefresh) -> TokenResponse:
    return refresh_tokens(refresh_token.token)
