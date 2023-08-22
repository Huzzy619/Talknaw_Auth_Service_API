from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, constr, conint, conlist, EmailStr


class User(BaseModel):
    username: constr(min_length=3)
    name: constr(min_length=3)
    email: EmailStr
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


class PasswordChange(BaseModel):
    current_password: str = None
    new_password: str


class GoogleAuthSchema(BaseModel):
    jwt_token: str

# class GoogleAuthResponse(BaseModel):
#     user: UserSchema
#     access_token: str




class OTPVerify(BaseModel):
    email: EmailStr
    otp: constr(min_length=6)
    