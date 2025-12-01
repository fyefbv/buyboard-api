from datetime import datetime, timezone

from fastapi import Request
from fastapi.responses import JSONResponse

from app.modules.ads.exceptions import (
    AdNotFoundError,
    AdPermissionError,
)


async def ad_not_found_handler(request: Request, exc: AdNotFoundError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": "ad_not_found",
                "message": exc.detail,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        },
    )


async def ad_permission_handler(request: Request, exc: AdPermissionError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": "ad_permission_denied",
                "message": exc.detail,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        },
    )
