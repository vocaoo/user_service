from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column
from uuid6 import uuid7

from .base import TimedBaseModel


class User(TimedBaseModel):
    __tablename__ = "users"
    __mapper_args__ = {"eager_defaults": True}

    user_id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid7)
    username: Mapped[str | None] = mapped_column(unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    middle_name: Mapped[str | None]
    department: Mapped[str | None]
    role: Mapped[str]
    photo_url: Mapped[str | None] = mapped_column(default=None)
    password: Mapped[str]
    deleted_at: Mapped[datetime | None] = mapped_column(default=None)
