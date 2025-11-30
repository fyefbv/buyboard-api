from datetime import datetime, timezone

from fastapi import Request
from fastapi.responses import JSONResponse

from app.modules.locations.exceptions import (
    LocationNotFoundError,
)


async def location_not_found_handler(request: Request, exc: LocationNotFoundError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": "location_not_found",
                "message": exc.detail,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        },
    )
