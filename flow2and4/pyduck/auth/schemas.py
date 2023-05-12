"""
This is the module for defining schemas related to pyduck auth.

[schemas]
UserVerificationEmailBase
    UserVerificationEmailCreate
    UserVerificationEmailRead
UserAvatarBase
    UserAvatarCrete
    UserAvatarRead
UserBackdropBase
    UserBackdropCreate
    UserBackdropRead
UserSnsBase
    UserSnsCreate
    UserSnsRead
UserBase
    UserRead
        UserReadForSession
    UserCreate
"""

from pydantic import Field
from datetime import datetime, timezone
from flow2and4.pyduck.schemas import PyduckSchema


class UserVerificationEmailBase(PyduckSchema):
    """Represent user verification email."""

    user_id: int
    vcode: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class UserVerificationEmailCreate(UserVerificationEmailBase):
    pass


class UserVerificationEmailRead(UserVerificationEmailBase):
    id: int


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


class UserBackdropBase(PyduckSchema):
    """Represent user backdrop base."""

    user_id: int
    url: str = "/auth/static/images/backdrop/default_backdrop.jpg"
    filename: str = "default_backdrop.jpg"
    original_filename: str = "default_backdrop.jpg"
    mimetype: str | None
    filesize: int | None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class UserBackdropCreate(UserBackdropBase):
    pass


class UserBackdropRead(UserBackdropBase):
    id: int


class UserSnsBase(PyduckSchema):
    """Represent user sns base."""

    user_id: int
    platform: str
    link: str
    public: bool
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class UserSnsCreate(UserSnsBase):
    pass


class UserSnsRead(UserSnsBase):
    id: int


class UserBase(PyduckSchema):
    """Represent user."""

    username: str
    nickname: str
    password: str
    active: bool = True
    verified: bool = False
    role: str = "user"
    about_me: str | None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    deleted_at: datetime | None


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int

    # relationship
    avatar: UserAvatarRead | None
    backdrop: UserBackdropRead | None
    sns: list[UserSnsRead | None]


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
