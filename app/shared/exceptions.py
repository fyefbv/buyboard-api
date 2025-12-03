from typing import Any

from fastapi import HTTPException, status


class NotFoundError(HTTPException):
    def __init__(self, entity_name: str, entity_field: Any = None):
        detail = (
            f"{entity_name} {entity_field} not found"
            if entity_field
            else f"{entity_name} not found"
        )
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
        self.entity_field = entity_field


class AlreadyExistsError(HTTPException):
    def __init__(self, entity_name: str, entity_field: Any = None):
        detail = (
            f"{entity_name} {entity_field} already exists"
            if entity_field
            else f"{entity_name} already exists"
        )
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
        self.entity_field = entity_field


class ObjectUploadError(HTTPException):
    def __init__(self, object_name: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload object {object_name}",
        )


class ObjectDeleteError(HTTPException):
    def __init__(self, object_name: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete object {object_name}",
        )


class ObjectListGetError(HTTPException):
    def __init__(self, object_name: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get the {object_name} object list",
        )


class UnsupportedMediaTypeError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail=detail
        )


class FileTooLargeError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_413_CONTENT_TOO_LARGE, detail=detail)
