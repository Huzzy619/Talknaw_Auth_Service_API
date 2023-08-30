# from database.models.common import TimestampModel, UUIDModel
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

# from app.database.db import Base


class Example:
    __tablename__ = "example"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    email: Mapped[str]
    message: Mapped[str]

    class Config:
        arbitrary_types_allowed = True

    def __repr__(self):
        return f"<ContactUs (id: {self.id})>"
