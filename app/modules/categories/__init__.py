from fastapi import FastAPI

from app.modules.categories.endpoints import categories_router
from app.modules.categories.exception_handlers import (
    category_not_found_handler,
)
from app.modules.categories.exceptions import (
    CategoryNotFoundError,
)


def setup_category_exception_handlers(app: FastAPI):
    app.add_exception_handler(CategoryNotFoundError, category_not_found_handler)
