from fastapi import Depends

from app.core.unit_of_work import UnitOfWork
from app.modules.users.services import UserService
from app.shared.dependencies import get_unit_of_work


async def get_user_service(uow: UnitOfWork = Depends(get_unit_of_work)) -> UserService:
    return UserService(uow)
