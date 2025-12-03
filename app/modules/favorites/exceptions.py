from typing import Any

from fastapi import HTTPException, status

from app.shared.exceptions import AlreadyExistsError, NotFoundError


class FavoriteNotFoundError(NotFoundError):
    def __init__(self, favorite_field: Any = None):
        super().__init__("Favorite", favorite_field)


class FavoriteAlreadyExistsError(AlreadyExistsError):
    def __init__(self, favorite_field: Any = None):
        super().__init__("Favorite", favorite_field)


class CannotFavoriteOwnAdError(HTTPException):
    def __init__(self):
        detail = "You cannot add your own ads to favorites"
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
