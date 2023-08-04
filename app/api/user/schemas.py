from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, constr, conint, conlist, EmailStr


class UserSchema(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: str
    password: str

    class Config:
        from_attributes = True


class APIKey(BaseModel):
    key: str


class Signup(BaseModel):
    first_name: constr(min_length=3)
    last_name: constr(min_length=3)
    email: EmailStr
    password: constr(min_length=8)

    
class Update(BaseModel):
    first_name: str
    last_name: str


class GoogleSchema(BaseModel):
    name: str
    email: str
    accessToken: str
    googleId: str
    id_token: str


class SignupResponse(Signup):
    id: UUID


class Login(BaseModel):
    email: str
    password: str

class Verify(BaseModel):
    password: str

class Email(BaseModel):
    email: str


class PasswordChange(BaseModel):
    cur_password: str
    new_password: str


class LoginResponse(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: str


class PeopleCreateSchema(BaseModel):
    name: str
    age: int
    gender: str
    occupation: List[str]
    vip_score: int
    is_vip: bool

class GoogleAuthSchema(BaseModel):
    jwt_token: str

class GoogleAuthResponse(BaseModel):
    user: UserSchema
    access_token: str


class UserDetail(BaseModel):
    user: LoginResponse
    access_token: str
    refresh_token: str
    
class RegistrationSuccess(BaseModel):
    data: UserDetail
    message: str
    status: str


class OTPVerify(BaseModel):
    email: EmailStr
    otp: constr(min_length=6)
    