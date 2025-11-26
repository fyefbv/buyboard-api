from datetime import datetime, timezone

from fastapi import Request
from fastapi.responses import JSONResponse

from app.modules.users.exceptions import (
    UserAlreadyExistsError,
    UserNotFoundError,
)


async def user_not_found_handler(request: Request, exc: UserNotFoundError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": "user_not_found",
                "message": exc.detail,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        },
    )


async def user_exists_handler(request: Request, exc: UserAlreadyExistsError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": "user_already_exists",
                "message": exc.detail,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        },
    )
