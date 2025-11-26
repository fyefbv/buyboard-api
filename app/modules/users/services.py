from uuid import UUID

from app.core.security import get_password_hash
from app.core.unit_of_work import UnitOfWork
from app.modules.users.exceptions import UserAlreadyExistsError, UserNotFoundError
from app.modules.users.schemas import UserCreate, UserLogin, UserResponse, UserUpdate


class UserService:

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def create_user(self, user_create: UserCreate) -> UserResponse:
        user_dict: dict = user_create.model_dump()
        user_dict["password_hash"] = get_password_hash(user_dict.pop("password"))
        async with self.uow as uow:
            existing_user = await uow.user.find_one(login=user_create.login)
            if existing_user:
                raise UserAlreadyExistsError(user_create.login)

            user = await uow.user.add_one(user_dict)
            user_to_return = UserResponse.model_validate(user)
            await uow.commit()

            return user_to_return

    async def get_user(self, user_id: UUID) -> UserResponse:
        async with self.uow as uow:
            user = await uow.user.get_by_id(user_id)
            if not user:
                raise UserNotFoundError(user_id)

            user_to_return = UserResponse.model_validate(user)

            return user_to_return

    async def update_user(self, user_id: UUID, user_update: UserUpdate) -> UserResponse:
        user_dict: dict = user_update.model_dump(exclude_unset=True)
        if "password" in user_dict:
            user_dict["password_hash"] = get_password_hash(user_dict.pop("password"))
        async with self.uow as uow:
            user = await uow.user.update(user_id, user_dict)
            if not user:
                raise UserNotFoundError(user_id)

            user_to_return = UserResponse.model_validate(user)
            await uow.commit()

            return user_to_return

    async def delete_user(self, user_id: UUID) -> None:
        async with self.uow as uow:
            user = await uow.user.get_by_id(user_id)
            if not user:
                raise UserNotFoundError(user_id)

            await uow.user.delete(user_id)
            await uow.commit()

    # async def get_users(self) -> list[UserResponse]:
    #     async with self.uow as uow:
    #         users = await uow.user.find_all()
    #         users_to_return = [UserResponse.model_validate(user) for user in users]

    #         return users_to_return
