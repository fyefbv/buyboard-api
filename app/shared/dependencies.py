from uuid import UUID

from fastapi import Depends

from app.core.unit_of_work import UnitOfWork
from app.modules.auth.auth import decode_jwt, oauth2_scheme
from app.modules.auth.exceptions import MissingTokenError


async def get_unit_of_work() -> UnitOfWork:
    return UnitOfWork()


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UUID:
    if not token:
        raise MissingTokenError()

    payload = decode_jwt(token)
    return UUID(payload.get("sub"))
