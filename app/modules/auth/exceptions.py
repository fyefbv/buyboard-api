from typing import Any

from fastapi import HTTPException, status

from app.shared.exceptions import AlreadyExistsError


class InvalidTokenError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )


class ExpiredTokenError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
        )


class MissingTokenError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )


class UserAlreadyExistsError(AlreadyExistsError):
    def __init__(self, user_field: Any = None):
        super().__init__("User", user_field)


class AuthenticationFailedError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed"
        )
