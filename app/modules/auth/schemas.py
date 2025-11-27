from pydantic import BaseModel, EmailStr


class AuthBase(BaseModel):
    login: str


class UserRegister(AuthBase):
    email: EmailStr
    password: str


class UserLogin(AuthBase):
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str


class TokenRefresh(BaseModel):
    token: str
