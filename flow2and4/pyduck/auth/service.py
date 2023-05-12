"""
This is the module for handling database transactions related to pyduck auth.
"""

from sqlalchemy import select
from flow2and4.database import db
from flow2and4.pyduck.auth.models import (
    User,
    UserBackdrop,
    UserSns,
    UserAvatar,
    UserVerificationEmail,
)
from flow2and4.pyduck.auth.schemas import (
    UserCreate,
    UserRead,
    UserReadForSession,
    UserAvatarCreate,
    UserAvatarRead,
    UserVerificationEmailCreate,
    UserVerificationEmailRead,
    UserBackdropCreate,
    UserBackdropRead,
    UserSnsCreate,
    UserSnsRead,
    UserAvatarUpdate,
    UserBackdropUpdate,
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

    avatar = UserAvatar(**avatar_in.dict())
    db.session.add(avatar)
    db.session.commit()

    return UserAvatarRead.from_orm(avatar)


def create_user_backdrop(*, backdrop_in: UserBackdropCreate) -> UserBackdropRead:
    """Insert user backdrop in table."""

    backdrop = UserBackdrop(**backdrop_in.dict())
    db.session.add(backdrop)
    db.session.commit()

    return UserBackdropRead.from_orm(backdrop)


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


def update_about_me(*, user_id: int, about_me: str) -> None:
    """Update user's about_me."""

    user = _get_user(user_id)
    setattr(user, "about_me", about_me)
    db.session.commit()


def delete_and_create_user_sns(
    *, user_id: int, snss_in: list[UserSnsCreate]
) -> list[UserSnsRead]:
    """Delete user's old sns and replace(create) it with new sns."""

    user = _get_user(user_id)
    user.sns = []

    snss = []
    for sns_in in snss_in:
        snss.append(UserSns(**sns_in.dict()))

    db.session.add_all(snss)
    db.session.commit()

    return [UserSnsRead.from_orm(sns) for sns in snss]


def _get_user_sns_by_user_id(*, user_id) -> list[UserSns | None]:
    """Get user sns by user id."""
    return db.session.scalars(select(UserSns).filter_by(user_id=user_id)).all()


def get_user_sns_by_user_id(*, user_id) -> list[UserSnsRead | None]:
    """Get user avatar by user id."""
    return [
        UserSnsRead.from_orm(sns) for sns in _get_user_sns_by_user_id(user_id=user_id)
    ]


def _get_user_avatar_by_user_id(*, user_id) -> UserAvatar:
    """Get user backdrop by user id."""
    return db.session.scalars(select(UserAvatar).filter_by(user_id=user_id)).one()


def get_user_avatar_by_user_id(*, user_id) -> UserAvatarRead:
    """Get user avatar by user id."""
    return _get_user_avatar_by_user_id(user_id=user_id)


def _get_user_backdrop_by_user_id(*, user_id) -> UserBackdrop:
    """Get user backdrop by user id."""
    return db.session.scalars(select(UserBackdrop).filter_by(user_id=user_id)).one()


def get_user_backdrop_by_user_id(*, user_id) -> UserBackdropRead:
    """Get user backdrop by user id."""
    return _get_user_backdrop_by_user_id(user_id=user_id)


def _get_user_backdrop(id) -> UserBackdrop:
    """Get user backdrop by id."""
    return db.session.scalars(select(UserBackdrop).filter_by(id=id)).one()


def update_user_backdrop(*, backdrop_in: UserBackdropUpdate) -> UserBackdropRead:
    """Update user's backdrop."""

    backdrop = _get_user_backdrop(backdrop_in.id)

    updated_data = backdrop_in.dict(
        exclude={
            "id",
        }
    )
    for column, value in updated_data.items():
        setattr(backdrop, column, value)

    db.session.commit()
    return UserBackdropRead.from_orm(backdrop)


def _get_user_avatar(id) -> UserAvatar:
    """Get user avatar by id."""
    return db.session.scalars(select(UserAvatar).filter_by(id=id)).one()


def update_user_avatar(*, avatar_in: UserAvatarUpdate) -> UserAvatarRead:
    """Update user's backdrop."""

    avatar = _get_user_avatar(avatar_in.id)

    updated_data = avatar_in.dict(
        exclude={
            "id",
        }
    )
    for column, value in updated_data.items():
        setattr(avatar, column, value)

    db.session.commit()
    return UserAvatarRead.from_orm(avatar)
