from typing import Optional
from uuid import UUID

from aredis_om import JsonModel
from pydantic import (  # , EmailStr#, conint, conlist,
    BaseModel,
    EmailStr,
    constr,
    validator,
    root_validator
)

from app.utils.helper import create_custom_username


class User(BaseModel):
    username: Optional[constr(min_length=3)]
    name: constr(min_length=3)
    email: EmailStr
    password: constr(min_length=8)
    picture: Optional[str] = None

    @root_validator(pre=True)
    def validate_username(cls, values, **kwargs):
        if values.get("username") is None:
            values["username"] = create_custom_username(values.get("name"))

        return values
    


class User2(JsonModel):
    username: constr(min_length=3)
    name: constr(min_length=3)
    email: str
    password: constr(min_length=8)
    picture: Optional[str] = None


class UserProfile(BaseModel):
    user_id: UUID


class UserTokenProfile(BaseModel):
    access_token: str
    refresh_token: str


class UserUpdate(User):
    ...


class Login(BaseModel):
    email: EmailStr
    password: constr(min_length=8)


class GoogleSchema(BaseModel):
    name: str
    email: str
    accessToken: str
    googleId: str
    id_token: str


class ResetPassword(BaseModel):
    new_password: str


class PasswordChange(ResetPassword):
    current_password: str


class GoogleAuthSchema(BaseModel):
    jwt_token: str


# class GoogleAuthResponse(BaseModel):
#     user: UserSchema
#     access_token: str


class OTPVerify(BaseModel):
    email: EmailStr
    otp: constr(min_length=6)

class MessageProfile(BaseModel):
    detail: str
    status: bool