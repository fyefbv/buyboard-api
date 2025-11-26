from datetime import datetime, timezone

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Обработчик для ошибок валидации Pydantic"""

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={
            "success": False,
            "error": {
                "code": "validation_error",
                "message": "Validation failed",
                "details": exc.errors(),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        },
    )


async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """Обработчик для ошибок базы данных"""

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "code": "database_error",
                "message": "Database error occurred",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        },
    )


async def general_exception_handler(request: Request, exc: Exception):
    """Обработчик для непредвиденных исключений"""

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "code": "internal_server_error",
                "message": "Internal server error",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        },
    )
