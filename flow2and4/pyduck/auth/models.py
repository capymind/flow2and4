"""
This is module for defining ORMs and tables related to auth.
"""
from __future__ import annotations
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flow2and4.database import db
from flow2and4.pyduck.models import ImageUploadMixin


class PyduckUserAvatar(ImageUploadMixin, db.Model):
    """Represent user avatar."""

    __bind_key__ = "pyduck"
    __tablename__ = "user_avatar"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("user.id"))
    created_at: Mapped[str]


class User(db.Model):
    """Represent user."""

    __bind_key__ = "pyduck"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[int] = mapped_column(unique=True)
    nickname: Mapped[int] = mapped_column(unique=True)
    password: Mapped[int]
    active: Mapped[bool]
    verified: Mapped[bool]
    role: Mapped[str]
    created_at: Mapped[str]
    deleted_at: Mapped[str | None]

    # relationship
    avatar: Mapped[PyduckUserAvatar] = relationship()


class UserVerificationEmail(db.Model):
    """Represent user verification email."""

    __bind_key__ = "pyduck"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("user.id"))
    vcode: Mapped[str]
    created_at: Mapped[str]

    # relationship
    user: Mapped[User] = relationship("pyduck.auth.models.User")
