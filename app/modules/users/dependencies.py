from fastapi import Depends

from app.core.dependencies import get_unit_of_work
from app.core.unit_of_work import UnitOfWork
from app.modules.users.services import UserService


async def get_user_service(uow: UnitOfWork = Depends(get_unit_of_work)) -> UserService:
    return UserService(uow)
