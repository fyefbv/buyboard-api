from datetime import datetime, timezone

from fastapi import Request
from fastapi.responses import JSONResponse

from app.modules.favorites.exceptions import (
    CannotFavoriteOwnAdError,
    FavoriteAlreadyExistsError,
    FavoriteNotFoundError,
)


async def favorite_not_found_handler(request: Request, exc: FavoriteNotFoundError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": "favorite_not_found",
                "message": exc.detail,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        },
    )


async def favorite_already_exists_handler(
    request: Request, exc: FavoriteAlreadyExistsError
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": "favorite_already_exists",
                "message": exc.detail,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        },
    )


async def cannot_favorite_own_ad_handler(
    request: Request, exc: CannotFavoriteOwnAdError
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": "cannot_favorite_own_ad",
                "message": exc.detail,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        },
    )
