"""
This is the module for handling database transactions related to pyduck auth.
"""

from sqlalchemy import select
from csduck.database import db
from csduck.pyduck.auth.models import User, PyduckUserAvatar, UserVerificationEmail
from csduck.pyduck.auth.schemas import (
    UserCreate,
    UserRead,
    UserReadForSession,
    UserAvatarCreate,
    UserAvatarRead,
    UserVerificationEmailCreate,
    UserVerificationEmailRead,
)


def does_field_value_exist(field: str, value: str | int | float) -> bool:
    """Check table column's value."""

    condition = getattr(User, field) == value
    return bool(db.session.scalars(select(User).where(condition)).one_or_none())


def create_user(*, user_in: UserCreate) -> UserRead:
    """Insert user in table."""

    user = User(**user_in.dict())
    db.session.add(user)
    db.session.commit()

    return UserRead.from_orm(user)


def _get_user(id: int) -> User | None:
    """Select user by id."""
    return db.session.scalars(select(User).filter_by(id=id)).one_or_none()


def get_pyduck_user_for_session(*, id: int) -> UserReadForSession:
    """Select user for sign-in session."""
    user = _get_user(id=id)
    return UserReadForSession.from_orm(user)


def get_user_by_username(*, username: str) -> UserReadForSession | None:
    """Select user by username for sign-in session."""

    user = db.session.scalars(select(User).filter_by(username=username)).one_or_none()

    return UserReadForSession.from_orm(user) if user is not None else None


def create_user_avatar(*, avatar_in: UserAvatarCreate) -> UserAvatarRead:
    """Insert user avatar in table."""

    avatar = PyduckUserAvatar(**avatar_in.dict())
    db.session.add(avatar)
    db.session.commit()

    return UserAvatarRead.from_orm(avatar)


def create_user_verification_email(
    *, verification_in: UserVerificationEmailCreate
) -> UserVerificationEmailRead:
    """Insert user verification email in table."""

    verification = UserVerificationEmail(**verification_in.dict())

    db.session.add(verification)
    db.session.commit()

    return UserVerificationEmailRead.from_orm(verification)


def get_user_verification_email(*, user_id: int) -> UserVerificationEmailRead | None:
    """Select user verification email."""

    verification = db.session.scalars(
        select(UserVerificationEmail).filter_by(user_id=user_id)
    ).one_or_none()

    return (
        UserVerificationEmailRead.from_orm(verification)
        if verification is not None
        else None
    )


def verify_user(*, user_id: int) -> UserRead:
    """Change user's verified to true(verified)."""

    user = _get_user(id=user_id)
    user.verified = True
    db.session.commit()

    return UserRead.from_orm(user)
