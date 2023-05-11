"""
This is the module for handling database transactions related to auth.

[functions(service)]

is_duplicate
create_user
create_user_email_verification
_get_user_by_username
get_user_by_username
_get_user
get_user_for_session
"""

from sqlalchemy import select
from flow2and4.auth.models import User, UserEmailVerification, UserAvatar
from flow2and4.auth.schemas import (
    UserCreate,
    UserRead,
    UserReadForSession,
    UserEmailVerificationCreate,
    UserEmailVerificationRead,
    UserAvatarCreate,
    UserAvatarRead,
)
from flow2and4.database import db


def is_duplicate(*, field: str, value: str):
    """Check whether specific field's value exists return True if exists else Flase."""

    condition = getattr(User, field) == value
    return bool(db.session.scalars(select(User).where(condition)).one_or_none())


def create_user(*, user_in: UserCreate) -> UserRead:
    """Insert user."""

    user = User(**user_in.dict())
    db.session.add(user)
    db.session.commit()

    return UserRead.from_orm(user)


def create_user_email_verification(
    *, user_email_verification_in: UserEmailVerificationCreate
) -> UserEmailVerificationRead:
    """Insert user email verification."""

    user_email_verification = UserEmailVerification(**user_email_verification_in.dict())
    db.session.add(user_email_verification)
    db.session.commit()

    return UserEmailVerificationRead.from_orm(user_email_verification)


def _get_user_by_username(*, username: str) -> User | None:
    """Select user by username."""
    return db.session.scalars(select(User).filter_by(username=username)).one_or_none()


def get_user_by_username(*, username: str) -> UserRead | None:
    """Select user by username."""

    user = _get_user_by_username(username=username)

    return UserRead.from_orm(user) if user is not None else user


def _get_user(id: int) -> User | None:
    """Select user by id."""
    return db.session.scalars(select(User).filter_by(id=id)).one_or_none()


def get_user_for_session(*, id: int) -> UserReadForSession | None:
    """Select user by id and return schema for session."""

    user = _get_user(id=id)
    return UserReadForSession.from_orm(user)


def create_user_avatar(*, user_avatar_in: UserAvatarCreate) -> UserAvatarRead:
    """Insert user avatar."""

    user_avatar = UserAvatar(**user_avatar_in.dict())
    db.session.add(user_avatar)
    db.session.commit()

    return UserAvatarRead.from_orm(user_avatar)
