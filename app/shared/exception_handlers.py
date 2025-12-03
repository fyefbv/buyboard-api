from datetime import datetime, timezone

from fastapi import Request
from fastapi.responses import JSONResponse

from app.shared.exceptions import (
    FileTooLargeError,
    ObjectDeleteError,
    ObjectListGetError,
    ObjectUploadError,
    UnsupportedMediaTypeError,
)


async def object_upload_handler(request: Request, exc: ObjectUploadError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": "object_upload_error",
                "message": exc.detail,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        },
    )


async def object_delete_handler(request: Request, exc: ObjectDeleteError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": "object_delete_error",
                "message": exc.detail,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        },
    )


async def object_list_get_handler(request: Request, exc: ObjectListGetError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": "object_list_get_error",
                "message": exc.detail,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        },
    )


async def unsupported_media_type_handler(
    request: Request, exc: UnsupportedMediaTypeError
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": "unsupported_media_type",
                "message": exc.detail,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        },
    )


async def file_too_large_handler(request: Request, exc: FileTooLargeError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": "file_too_large",
                "message": exc.detail,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        },
    )
