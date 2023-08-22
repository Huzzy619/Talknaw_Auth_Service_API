from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Body, Depends, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import EmailStr

from app.api.user.authentication import refreshJWT
from app.api.user.otp import OTPGenerator
from app.api.user.schemas import (
    Login,
    OTPVerify,  # GoogleAuthSchema,
    PasswordChange,
    User,
    UserTokenProfile,
)
from app.api.user.services import UserService
from app.api.user.tasks import create_profile
from app.database.db import AnSession

router = APIRouter(tags=["Auth-Routes"], prefix="/accounts")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
auth_handler = UserService(session=AnSession)


@router.get("/check/username/{username}")
async def check_username_availability(username: str, session: AnSession):
    user_service = UserService(session=session)

    if await user_service.find_by_username(username=username):
        return {"detail": "unavailable", "status": False}

    return {"detail": "available", "status": True}


@router.get("/otp/send/{email}")
async def get_otp(email: EmailStr, session: AnSession):
    user_service = UserService(session=session)

    user = await user_service.find_by_email(email=email)
    otp_gen = OTPGenerator(user_id=user.id, session=session)

    otp = await otp_gen.get_otp()

    return {"code": otp}


@router.post("/otp/verify")
async def verify_otp(otp_data: OTPVerify, session: AnSession):
    user_service = UserService(session=session)
    user = await user_service.find_by_email(email=otp_data.email)

    otp_gen = OTPGenerator(user_id=user.id, session=session)

    status = await otp_gen.check_otp(otp=otp_data.otp)

    return {"status": status}


@router.post(
    "/signup", status_code=status.HTTP_201_CREATED, response_model=UserTokenProfile
)
async def create_user(
    user: User, session: AnSession, background_tasks: BackgroundTasks
):
    user_service = UserService(session=session)

    result = await user_service.create_user(user)

    background_tasks.add_task(create_profile, result)

    return result


@router.post("/login", response_model=UserTokenProfile)
async def login(user: Login, session: AnSession):
    user_service = UserService(session=session)
    return await user_service.login_user(user)


@router.post("/refresh_token", response_model=UserTokenProfile)
async def refresh_token(
    refresh_token: Annotated[str, Body(embed=True)]  # = Depends(JWTBearer(refresh=True)
):
    access_token = refreshJWT(refresh_token)
    user_id = UserService().decode_token(token=access_token)

    return {
        "user_id": user_id,
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


@router.post("/change_password", status_code=201)
async def change_user_password(
    form_data: PasswordChange,
    session: AnSession,
    user_id=Depends(auth_handler.auth_wrapper),
):
    user_service = UserService(session=session)
    return await user_service.change_password(user_id=user_id, **form_data.model_dump())


@router.get("/forgot/password/{email}")
async def verify_email(email: EmailStr, session: AnSession):
    user_service = UserService(session=session)
    await user_service.forgot_password(email)
    return {"detail": "email has been sent to provided address"}


@router.post("/reset_password/{email}")
async def reset_password(email: EmailStr, password: PasswordChange, session: AnSession):
    user_service = UserService(session=session)
    response = await user_service.password_reset(email, password)
    return response
