from typing import Any

from app.shared.exceptions import NotFoundError


class CategoryNotFoundError(NotFoundError):
    def __init__(self, category_field: Any = None):
        super().__init__("Category", category_field)
