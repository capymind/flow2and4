"""
This is the module for defining schemas related to auth.

[schemas]
UserBase
    UserCreate
    UserRead
    UserReadForSession
UserEmailVerificationBase
    UserEmailVerificationCreate
    UserEmailVerificationRead
UserAvatarBase
    UserAvatarCreate
    UserAvatarRead
"""

from datetime import datetime, timezone
from flow2and4.schemas import BaseSchema
from pydantic import Field


class UserAvatarBase(BaseSchema):
    """Represent user avatar base."""

    user_id: int
    url: str = "/auth/static/images/avatars/default_avatar.jpg"  # HACK: hard-coded
    filename: str = "default_avatar.jpg"
    original_filename: str = "default_avatar.jpg"
    filesize: int = 54
    mimetype: str = "image/jpeg"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime | None


class UserAvatarCreate(UserAvatarBase):
    pass


class UserAvatarRead(UserAvatarBase):
    id: int


class UserBase(BaseSchema):
    """Represent user base."""

    username: str
    nickname: str
    password: str
    active: bool = True
    verified: bool = False
    role: str = "user"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    deleted_at: datetime | None


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int


class UserEmailVerificationBase(BaseSchema):
    """Represent user email verificaton."""

    user_id: int
    vcode: str
    verified: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class UserEmailVerificationCreate(UserEmailVerificationBase):
    pass


class UserEmailVerificationRead(UserEmailVerificationBase):
    id: int


class UserReadForSession(UserRead):
    """Represent user for session used by flask_login."""

    @property
    def is_active(self):
        return self.active

    @property
    def is_authenticated(self):
        return self.verified

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    # relationship.
    avatar: UserAvatarRead
