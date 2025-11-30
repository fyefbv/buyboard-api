from typing import Any

from app.shared.exceptions import NotFoundError


class LocationNotFoundError(NotFoundError):
    def __init__(self, location_field: Any = None):
        super().__init__("Location", location_field)
