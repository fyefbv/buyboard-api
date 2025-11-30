from fastapi import FastAPI

from app.modules.locations.endpoints import locations_router
from app.modules.locations.exceptions import (
    LocationNotFoundError,
)
from app.modules.locations.exceptions_handlers import (
    location_not_found_handler,
)


def setup_location_exception_handlers(app: FastAPI):
    """Настройка обработчиков исключений локаций"""

    app.add_exception_handler(LocationNotFoundError, location_not_found_handler)
