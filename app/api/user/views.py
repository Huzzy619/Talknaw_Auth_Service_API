from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Body, Depends, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import EmailStr

from app.api.user.authentication import refreshJWT
from app.api.user.otp import OTPGenerator
from app.api.user.schemas import (
    Login,
    MessageProfile,
    OTPVerify,
    PasswordChange,
    ResetPassword,
    User,
    User2,
    UserTokenProfile,
)
from app.api.user.services import UserService
from app.api.user.tasks import create_profile
from app.database.db import AnSession

router = APIRouter(tags=["Auth-Routes"], prefix="/api/v1/accounts")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
auth_handler = UserService(session=AnSession)


@router.get("/check/username/{username}", response_model=MessageProfile)
async def check_username_availability(username: str, session: AnSession):
    user_service = UserService(session=session)
    return await user_service.find_by_username(username=username)


@router.get("/otp/send/{email}", response_model=MessageProfile)
async def get_otp(email: EmailStr, session: AnSession):
    user_service = UserService(session=session)

    user = await user_service.find_by_email(email=email)
    otp_gen = OTPGenerator(user_id=user.id, session=session)

    otp = await otp_gen.get_otp()

    return {"detail": "OTP has been sent to your email", "status": True}


@router.post("/otp/verify", response_model=MessageProfile)
async def verify_otp(otp_data: OTPVerify, session: AnSession):
    user_service = UserService(session=session)
    user = await user_service.find_by_email(email=otp_data.email)

    otp_gen = OTPGenerator(user_id=user.id, session=session)

    message, status = await otp_gen.check_otp(otp=otp_data.otp)

    return {"detail": message, "status": status}


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


# @router.post(
#     "/signup2", status_code=status.HTTP_201_CREATED
# )
async def create_user2(
    user: User, session: AnSession, background_tasks: BackgroundTasks
):
    # user_service = UserService(session=session)

    # result = await user_service.create_user(user)

    # background_tasks.add_task(create_profile, result)
    user2 = User2(**user.model_dump())
    await user2.save()

    data = await User2.all_pks()
    print(data)
    return {"result": [item for item in data]}


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


@router.patch("/change_password", response_model=MessageProfile)
async def change_user_password(
    form_data: PasswordChange,
    session: AnSession,
    user_id=Depends(auth_handler.auth_wrapper),
):
    user_service = UserService(session=session)
    return await user_service.change_password(user_id=user_id, **form_data.model_dump())


@router.get("/forgot_password/{email}", response_model=MessageProfile)
async def verify_email(email: EmailStr, session: AnSession):
    user_service = UserService(session=session)
    return await user_service.forgot_password(email)


@router.post("/reset_password/{email}", response_model=MessageProfile)
async def reset_password(email: EmailStr, password: ResetPassword, session: AnSession):
    user_service = UserService(session=session)
    return await user_service.password_reset(email, password)
