from fastapi import APIRouter

from app.modules.auth import auth_router, setup_auth_exception_handlers
from app.modules.users import setup_user_exception_handlers, users_router

api_router = APIRouter(prefix="/api")

api_router.include_router(users_router)
api_router.include_router(auth_router)
