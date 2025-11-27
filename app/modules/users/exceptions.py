from typing import Any

from app.shared.exceptions import NotFoundError


class UserNotFoundError(NotFoundError):
    def __init__(self, user_field: Any = None):
        super().__init__("User", user_field)
