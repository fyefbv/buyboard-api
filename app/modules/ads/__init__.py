from fastapi import FastAPI

from app.modules.ads.endpoints import ads_router
from app.modules.ads.exception_handlers import (
    ad_not_found_handler,
    ad_permission_handler,
)
from app.modules.ads.exceptions import AdNotFoundError, AdPermissionError


def setup_ad_exception_handlers(app: FastAPI):
    app.add_exception_handler(AdNotFoundError, ad_not_found_handler)
    app.add_exception_handler(AdPermissionError, ad_permission_handler)
