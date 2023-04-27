"""
This is the model for defining ORMs and tables related to auth.
"""

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from csduck.database import db
from csduck.models import ImageUploadMixin


class User(db.Model):
    """Represent user."""

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[int] = mapped_column(unique=True)
    nickname: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    active: Mapped[bool]
    verified: Mapped[bool]
    role: Mapped[str]
    created_at: Mapped[str]
    deleted_at: Mapped[str | None]

    # relationship
    avatar: Mapped["UserAvatar"] = relationship()


class UserAvatar(ImageUploadMixin, db.Model):
    """Represent user avatar."""

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("user.id"))
    created_at: Mapped[str]
    updated_at: Mapped[str | None]


class UserEmailVerification(db.Model):
    """Represent user email verification."""

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("user.id"))
    vcode: Mapped[str]
    verified: Mapped[bool]
    created_at: Mapped[str]