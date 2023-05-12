"""
This is module for defining ORMs and tables related to auth.

[models]
UserAvatar
UserBackdrop
UserSns
User
UserVerificationEmail
"""
from __future__ import annotations
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flow2and4.database import db
from flow2and4.pyduck.models import ImageUploadMixin


class UserAvatar(ImageUploadMixin, db.Model):
    """Represent user avatar."""

    __bind_key__ = "pyduck"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), unique=True)
    created_at: Mapped[str]


class UserBackdrop(ImageUploadMixin, db.Model):
    """Represent user backdrop."""

    __bind_key__ = "pyduck"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), unique=True)
    created_at: Mapped[str]


class UserSns(db.Model):
    """Represent user sns."""

    __bind_key__ = "pyduck"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    platform: Mapped[str]
    link: Mapped[str]
    public: Mapped[bool]
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
    about_me: Mapped[str | None]
    created_at: Mapped[str]
    deleted_at: Mapped[str | None]

    # relationship
    avatar: Mapped[UserAvatar] = relationship(
        "pyduck.auth.models.UserAvatar", cascade="all, delete-orphan"
    )
    backdrop: Mapped[UserBackdrop] = relationship(
        "pyduck.auth.models.UserBackdrop", cascade="all, delete-orphan"
    )
    sns: Mapped[list[UserSns]] = relationship(
        "pyduck.auth.models.UserSns", cascade="all, delete-orphan"
    )


class UserVerificationEmail(db.Model):
    """Represent user verification email."""

    __bind_key__ = "pyduck"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), unique=True)
    vcode: Mapped[str]
    created_at: Mapped[str]

    # relationship
    user: Mapped[User] = relationship("pyduck.auth.models.User")
