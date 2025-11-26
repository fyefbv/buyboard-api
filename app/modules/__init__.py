from fastapi import APIRouter

from app.modules.users import setup_user_exception_handlers, users_router

api_router = APIRouter()

api_router.include_router(users_router)
