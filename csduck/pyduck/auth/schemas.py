"""
This is the module for defining schemas related to pyduck auth.
"""

from pydantic import Field
from datetime import datetime, timezone
from csduck.pyduck.schemas import PyduckSchema


class UserAvatarBase(PyduckSchema):
    """Represent user abatar."""

    user_id: int
    url: str = "/auth/static/images/avatar/default_avatar.jpg"
    filename: str = "default_avatar.jpg"
    original_filename: str = "default_avatar.jpg"
    mimetype: str | None
    filesize: int | None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class UserAvatarCreate(UserAvatarBase):
    pass


class UserAvatarRead(UserAvatarBase):
    id: int


class UserBase(PyduckSchema):
    """Represent user."""

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

    # relationship
    avatar: UserAvatarRead


class UserReadForSession(UserRead):
    """Represent user for session used by flask_login."""

    @property
    def is_active(self):
        return self.active

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
