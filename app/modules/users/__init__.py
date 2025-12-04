from fastapi import FastAPI

from app.modules.users.endpoints import users_router
from app.modules.users.exception_handlers import (
    user_not_found_handler,
)
from app.modules.users.exceptions import (
    UserNotFoundError,
)


def setup_user_exception_handlers(app: FastAPI):
    app.add_exception_handler(UserNotFoundError, user_not_found_handler)
