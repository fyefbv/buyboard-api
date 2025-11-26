from typing import Any

from app.core.exceptions import AlreadyExistsError, NotFoundError


class UserNotFoundError(NotFoundError):
    def __init__(self, user_field: Any = None):
        super().__init__("User", user_field)


class UserAlreadyExistsError(AlreadyExistsError):
    def __init__(self, user_field: Any = None):
        super().__init__("User", user_field)
