from fastapi import FastAPI

from app.modules.favorites.endpoints import favorites_router
from app.modules.favorites.exceptions import (
    CannotFavoriteOwnAdError,
    FavoriteAlreadyExistsError,
    FavoriteNotFoundError,
)
from app.modules.favorites.exceptions_handlers import (
    cannot_favorite_own_ad_handler,
    favorite_already_exists_handler,
    favorite_not_found_handler,
)


def setup_favorite_exception_handlers(app: FastAPI):
    """Настройка обработчиков исключений для избранного"""

    app.add_exception_handler(FavoriteNotFoundError, favorite_not_found_handler)
    app.add_exception_handler(
        FavoriteAlreadyExistsError, favorite_already_exists_handler
    )
    app.add_exception_handler(CannotFavoriteOwnAdError, cannot_favorite_own_ad_handler)
