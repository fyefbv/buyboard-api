from fastapi import FastAPI

from app.modules.locations.endpoints import locations_router
from app.modules.locations.exception_handlers import (
    location_not_found_handler,
)
from app.modules.locations.exceptions import (
    LocationNotFoundError,
)


def setup_location_exception_handlers(app: FastAPI):
    app.add_exception_handler(LocationNotFoundError, location_not_found_handler)
