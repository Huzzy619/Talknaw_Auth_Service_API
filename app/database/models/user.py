from sqlalchemy.orm import Mapped, mapped_column
from app.database.db import Base
from app.database.models.common import UUIDMixin
from uuid import UUID

class User(UUIDMixin, Base):
    __tablename__ = "users"

    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]

    def __repr__(self):
        return f"<User (id: {self.id})>"

class OTP(UUIDMixin, Base):

    counter: Mapped[int] = mapped_column(default=1)
    user_id: Mapped[UUID] 