from fastapi import FastAPI

from app.modules.users.endpoints import users_router
from app.modules.users.exceptions import (
    UserNotFoundError,
)
from app.modules.users.exceptions_handlers import (
    user_not_found_handler,
)


def setup_user_exception_handlers(app: FastAPI):
    """Настройка пользовательских обработчиков исключений"""

    app.add_exception_handler(UserNotFoundError, user_not_found_handler)
