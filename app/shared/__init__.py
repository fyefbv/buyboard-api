from fastapi import FastAPI

from app.shared.exception_handlers import (
    file_too_large_handler,
    object_delete_handler,
    object_list_get_handler,
    object_upload_handler,
    unsupported_media_type_handler,
)
from app.shared.exceptions import (
    FileTooLargeError,
    ObjectDeleteError,
    ObjectListGetError,
    ObjectUploadError,
    UnsupportedMediaTypeError,
)


def setup_shared_exception_handlers(app: FastAPI):
    app.add_exception_handler(ObjectUploadError, object_upload_handler)
    app.add_exception_handler(ObjectDeleteError, object_delete_handler)
    app.add_exception_handler(ObjectListGetError, object_list_get_handler)
    app.add_exception_handler(FileTooLargeError, file_too_large_handler)
    app.add_exception_handler(UnsupportedMediaTypeError, unsupported_media_type_handler)
