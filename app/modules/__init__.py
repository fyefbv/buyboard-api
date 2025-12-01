from fastapi import APIRouter

from app.modules.ads import ads_router, setup_ad_exception_handlers
from app.modules.auth import auth_router, setup_auth_exception_handlers
from app.modules.categories import categories_router, setup_category_exception_handlers
from app.modules.locations import locations_router, setup_location_exception_handlers
from app.modules.users import setup_user_exception_handlers, users_router

api_router = APIRouter(prefix="/api")

api_router.include_router(users_router)
api_router.include_router(auth_router)
api_router.include_router(categories_router)
api_router.include_router(locations_router)
api_router.include_router(ads_router)
