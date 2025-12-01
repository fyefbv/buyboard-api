from fastapi import Depends

from app.core.unit_of_work import UnitOfWork
from app.modules.auth.services import AuthService


async def get_unit_of_work() -> UnitOfWork:
    return UnitOfWork()


async def get_auth_service(uow: UnitOfWork = Depends(get_unit_of_work)) -> AuthService:
    return AuthService(uow)
