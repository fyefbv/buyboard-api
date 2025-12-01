from typing import Any

from fastapi import HTTPException, status

from app.shared.exceptions import NotFoundError


class AdNotFoundError(NotFoundError):
    def __init__(self, ad_field: Any = None):
        super().__init__("Ad", ad_field)


class AdPermissionError(HTTPException):
    def __init__(self, ad_field: Any = None):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                f"Permission denied for ad {ad_field}"
                if ad_field
                else f"Permission denied for ad"
            ),
        )
