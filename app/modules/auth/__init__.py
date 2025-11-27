from fastapi import FastAPI

from app.modules.auth.endpoints import auth_router
from app.modules.auth.exceptions import (
    AuthenticationFailedError,
    ExpiredTokenError,
    InvalidTokenError,
    MissingTokenError,
    UserAlreadyExistsError,
)
from app.modules.auth.exceptions_handlers import (
    authentication_failed_handler,
    expired_token_handler,
    invalid_token_handler,
    missing_token_handler,
    user_already_exists_handler,
)


def setup_auth_exception_handlers(app: FastAPI):
    """Настройка обработчиков исключений аутентификации"""

    app.add_exception_handler(AuthenticationFailedError, authentication_failed_handler)
    app.add_exception_handler(InvalidTokenError, invalid_token_handler)
    app.add_exception_handler(ExpiredTokenError, expired_token_handler)
    app.add_exception_handler(MissingTokenError, missing_token_handler)
    app.add_exception_handler(UserAlreadyExistsError, user_already_exists_handler)
