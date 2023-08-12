import base64
from datetime import datetime, timedelta

from pyotp import HOTP
from sqlalchemy import select, update

from app.core.config import settings
from app.database.db import AnSession
from app.database.models.user import OTP


class OTPGenerator:
    """
    secret_key(Base32): is needed to generate and verify the otp securely
    processed_id: is the first 4 digit of a UUID object type casted to Integer
    counter: keeps track of otp request made by a user.
    value: makes each request unique by adding processed_id and counter
    """

    def __init__(self, user_id, session: AnSession, **kwargs) -> None:
        self.secret_key = self.get_secret()
        self.user_id = user_id
        self.processed_id = int(str(int(user_id))[:4])
        self.hotp = HOTP(self.secret_key, digits=6)
        self.session = session

    # async def
    async def get_otp(self):
        otp_obj = await self.get_otp_obj(user_id=self.user_id)
        value = self.processed_id + otp_obj.counter
        otp = self.hotp.at(value)

        new_counter = otp_obj.counter + 1
        await self.session.execute(
            update(OTP)
            .where(OTP.user_id == self.user_id)
            .values(counter=new_counter, date_created=datetime.now())
        )
        await self.session.commit()
        return otp

    async def check_otp(self, otp):
        # convert otp_time to datetime object to enable subtraction
        otp_obj = await self.get_otp_obj(user_id=self.user_id)
        otp_time = otp_obj.date_created
        current_time = datetime.now()

        time_check = current_time - otp_time <= timedelta(minutes=5)

        # get the previous counter associated with a user and evaluate to get value
        value = self.processed_id + (otp_obj.counter - 1)
        verify_status = self.hotp.verify(otp, value)

        if verify_status and time_check:
            return "passed"
        elif verify_status and not time_check:
            return "expired"
        else:
            return "invalid"

    async def get_otp_obj(self, user_id, **kwargs):
        stmt = select(OTP).where(OTP.user_id == user_id)
        otp_obj = (await self.session.execute(stmt)).scalar_one_or_none()

        if not otp_obj:
            otp_obj = OTP(user_id=user_id)
            self.session.add(otp_obj)
            await self.session.commit()
            await self.session.refresh(otp_obj)

        return otp_obj

    def get_secret(self):
        """
        # Note: the otp_auth scheme DOES NOT use base32 padding for secret lengths not divisible by 8.
        # Some third-party tools have bugs when dealing with such secrets.
        # We might consider warning the user when generating a secret of length not divisible by 8.

        """
        string = getattr(settings, "secret_key")

        base32_encoded = base64.b32encode(string.encode("utf-8"))

        secret = base32_encoded.decode("utf-8")

        return secret[:32]
