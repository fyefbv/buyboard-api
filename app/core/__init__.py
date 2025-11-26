from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.core.system_exception_handlers import (
    general_exception_handler,
    sqlalchemy_exception_handler,
    validation_exception_handler,
)


def setup_system_exception_handlers(app: FastAPI):
    """Настройка системных обработчиков исключений"""

    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
