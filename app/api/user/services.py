from datetime import datetime, timedelta

from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.api.user.authentication import generate_jwt_pair
from app.api.user.schemas import GoogleSchema, Login, PasswordChange, User
from app.core.config import settings
from app.database.db import AnSession
from app.database.models.user import User

pwd_crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")
config_credentials = {
    "SECRET_KEY": settings.secret_key,
    "ALGORITHM": "HS256",
    "ACCESS_TOKEN_EXPIRE_MINUTES": timedelta(days=7).total_seconds(),
}
security = HTTPBearer()

authorized_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid Email or Password",
    headers={"WWW-Authenticate": "Bearer"},
)


class UserService:
    def __init__(self, session: AnSession = None):
        self.session = session

    def get_password_hash(self, password):
        return pwd_crypt.hash(password)

    async def verify_password(self, plain_password, hashed_password):
        return pwd_crypt.verify(plain_password, hashed_password)

    def encode_token(self, data: dict, expires_delta=None):
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        data["exp"] = expire
        encoded_jwt = jwt.encode(
            data,
            config_credentials["SECRET_KEY"],
            algorithm=config_credentials["ALGORITHM"],
        )
        return encoded_jwt

    def decode_token(self, token):
        try:
            payload = jwt.decode(
                token,
                config_credentials["SECRET_KEY"],
                algorithms=config_credentials["ALGORITHM"],
            )
            return payload["sub"]
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Signature has expired")
        except (JWTError, AttributeError):
            raise HTTPException(status_code=401, detail="Invalid token")

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(token=auth.credentials)

    async def create_user(self, user: User) -> User:
        statement = select(User).where(User.email == user.email)
        user_details = await self.session.execute(statement)
        user_details = user_details.scalar_one_or_none()
        if user_details:
            raise HTTPException(
                status_code=400, detail="email already exist, please try a new one"
            )
        else:
            try:
                password = self.get_password_hash(user.password)
                user.password = password
                new_user = User(**user.model_dump())
                self.session.add(new_user)
                await self.session.commit()
                await self.session.refresh(new_user)

            except IntegrityError:
                raise HTTPException(status_code=400, detail="Username is already taken")

            access_token, refresh_token = await generate_jwt_pair(
                new_user.id, new_user.email
            )

            data = {
                "user_id": new_user.id,
                "access_token": access_token,
                "refresh_token": refresh_token,
            }

            # automatically subscribe users upon registration
            # await SubscriberService(session=self.session).subscribe_email(user)

            return data

    async def login_user(self, login_data: Login):
        user = await self.authenticate_user(login_data.email, login_data.password)

        if user is None:
            raise HTTPException(status_code=401, detail="Invalid Email or Password")
        access_token, refresh_token = await generate_jwt_pair(user.id, user.email)
        data = {
            "user_id": user.id,
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
        return data

    async def authenticate_user(self, email, password):
        statement = select(User).where(User.email == email)
        user = await self.session.execute(statement)
        user = user.scalar_one_or_none()
        if user and await self.verify_password(password, user.password):
            return user

        return None

    async def change_password(self, user_id, current_password, new_password):
        from uuid import UUID

        statement = select(User).where(User.id == UUID(user_id))
        user = (await self.session.execute(statement)).scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=401, detail="User does not exist")

        # check if current password matches
        verify_password = pwd_crypt.verify(current_password, user.password)
        if not verify_password:
            raise HTTPException(
                status_code=401, detail="Current password does not match"
            )
        # check if new password matches old password
        check_password = pwd_crypt.verify(new_password, user.password)
        if check_password:
            raise HTTPException(
                status_code=401,
                detail="You have used this password before, try a new one",
            )

        _password = self.get_password_hash(new_password)
        user.password = _password
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return {"detail": "Password was updated successfully"}

    async def google_create_user(self, user: GoogleSchema):
        statement = select(User).where(User.email == user.email)
        user_details = await self.session.execute(statement)
        user_details = user_details.scalars().first()
        if user_details:
            raise HTTPException(
                status_code=400, detail="email already exist, please try a new one"
            )

        user_details.first_name = user.name
        user_details.last_name = user.googleId
        user_details.email = user.email
        user_details.password = user.accessToken
        new_user = User(**user.dict())
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return self.success("Registration was successful", new_user)

    async def google_authenticate(self, user):
        """
        Generates access_token for a google verified user

        Args:
        user: User Model Instance

        Return:
        access_token: generated access token
        """

        if not user:
            raise authorized_exception
        tokens = await self.create_token(user)
        return tokens

    async def create_token(self, user):
        access_token, refresh_token = await generate_jwt_pair(user.id, user.email)

        return access_token, refresh_token

    async def find_by_email(self, email):
        """
        Find a user by Email

        Args:
        email: user email address

        Return:
            User: Found User Object
                or
            None
        """
        statement = select(User).where(User.email == email)
        user = await self.session.execute(statement)
        found_user = user.scalar_one_or_none()

        if found_user:
            return found_user

        raise HTTPException(detail="User not Found", status_code=401)

    async def find_by_username(self, username):
        statement = select(User).where(User.username == username)
        user = (await self.session.execute(statement)).scalar_one_or_none()

        if user:
            return user

        return None

    async def forgot_password(self, email):
        try:
            await self.find_by_email(email=email)
            # Contact the service to send Email

        except HTTPException:
            pass

        return

    async def password_reset(self, email, password: PasswordChange):
        user = self.find_by_email(email)

        _password = self.get_password_hash(password.new_password)
        user.password = _password
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return {"detail": "Password was updated successfully"}

    async def find_by_id(self, id):
        """
        Find a user by Email

        Args:
        email: user email address

        Return:
            User: Found User Object
                or
            None
        """
        statement = select(User).where(User.id == id)
        try:
            user = await self.session.execute(statement)
            found_user = user.scalars().first()
            return found_user
        except Exception as e:
            print(e)
            return None
