from datetime import datetime, timezone

from fastapi import Request
from fastapi.responses import JSONResponse

from app.modules.categories.exceptions import (
    CategoryNotFoundError,
)


async def category_not_found_handler(request: Request, exc: CategoryNotFoundError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": "category_not_found",
                "message": exc.detail,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        },
    )
