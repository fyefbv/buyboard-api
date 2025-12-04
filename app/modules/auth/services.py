from app.core.security import get_password_hash, verify_password
from app.core.unit_of_work import UnitOfWork
from app.modules.auth.auth import create_tokens
from app.modules.auth.exceptions import (
    AuthenticationFailedError,
    UserAlreadyExistsError,
)
from app.modules.auth.schemas import TokenResponse, UserLogin, UserRegister


class AuthService:

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def register_user(self, user_register: UserRegister) -> TokenResponse:
        user_dict: dict = user_register.model_dump()
        user_dict["password_hash"] = get_password_hash(user_dict.pop("password"))
        async with self.uow as uow:
            existing_by_login = await uow.user.find_one(login=user_register.login)
            if existing_by_login:
                raise UserAlreadyExistsError(user_register.login)

            existing_by_email = await uow.user.find_one(email=user_register.email)
            if existing_by_email:
                raise UserAlreadyExistsError(user_register.email)

            user = await uow.user.add_one(user_dict)

            await uow.commit()

            return create_tokens(user.id)

    async def authenticate_user(self, user_login: UserLogin) -> TokenResponse:
        async with self.uow as uow:
            user = await uow.user.find_one(login=user_login.login)
            if not user or not verify_password(user_login.password, user.password_hash):
                raise AuthenticationFailedError()

            return create_tokens(user.id)
