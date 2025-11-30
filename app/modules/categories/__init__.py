from fastapi import FastAPI

from app.modules.categories.endpoints import categories_router
from app.modules.categories.exceptions import (
    CategoryNotFoundError,
)
from app.modules.categories.exceptions_handlers import (
    category_not_found_handler,
)


def setup_category_exception_handlers(app: FastAPI):
    """Настройка обработчиков исключений категорий"""

    app.add_exception_handler(CategoryNotFoundError, category_not_found_handler)
