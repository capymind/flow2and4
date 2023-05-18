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
    UserBackdropUpdate
    UserBackdropRead
UserSnsBase
    UserSnsCreate
    UserSnsRead
UserBase
    UserRead
        UserReadForSession
    UserCreate
UserActionBase
    UserActionVoteBase
        UserActionVotePostBase
            UserActionVotePostCreate
            UserActionVotePostRead
        UserActionVotePostCommentBase
            UserActionVotePostCommentCreate
            UserActionVotePostComentRead
        UserActionVoteQuestionBase
            UserActionVoteQuestionCreate
            UserActionVoteQuestionRead
        UserActionVoteAnswerBase
            UserActionVoteAnswerCreate
            UserActionVoteAnswerRead
        UserActionVoteAnswerCommentBase
            UserActionVoteAnswerCommentCreate
            UserActionVoteAnswerCommentRead        
    UserActionReactionBase
        UserActionReactionPostBase
            UserActionReactionPostCreate
            UserActionReactionPostRead
        UserActionReactionPostCommentBase
            UserActionReactionPostCommentCreate
            UserActionReactionPostComentRead
        UserActionReactionQuestionBase
            UserActionReactionQuestionCreate
            UserActionReactionQuestionRead
        UserActionReactionAnswerBase
            UserActionReactionAnswerCreate
            UserActionReactionAnswerRead
        UserActionReactionAnswerCommentBase
            UserActionReactionAnswerCommentCreate
            UserActionReactionAnswerCommentRead
"""

from datetime import datetime, timezone

from pydantic import Field

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


class UserAvatarUpdate(UserAvatarBase):
    id: int


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


class UserBackdropUpdate(UserBackdropBase):
    id: int


class UserBackdropRead(UserBackdropBase):
    id: int


class UserSnsBase(PyduckSchema):
    """Represent user sns base."""

    user_id: int
    platform: str
    link: str = ""
    public: bool = False
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


class UserActionBase(PyduckSchema):
    """Represent base schema for user action."""

    user_id: int
    action_type: str
    action_value: str | None
    target_id: int | None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class UserActionCreatePostBase(UserActionBase):
    """Represent base schema for user action that user create a post."""

    action_type: str = "create_post"


class UserActionCreatePostCreate(UserActionCreatePostBase):
    pass


class UserActionCreatePostRead(UserActionCreatePostBase):
    id: int


class UserActionCreatePostCommentBase(UserActionBase):
    """Represent base schema for user action that user create a comment in a post."""

    action_type: str = "create_post_comment"


class UserActionCreatePostCommentCreate(UserActionCreatePostCommentBase):
    pass


class UserActionCreatePostCommentRead(UserActionCreatePostCommentBase):
    id: int


class UserActionCreateQuestionBase(UserActionBase):
    """Represent base schema for user action that user create a question."""

    action_type: str = "create_question"


class UserActionCreateQuestionCreate(UserActionCreateQuestionBase):
    pass


class UserActionCreateQuestionRead(UserActionCreateQuestionBase):
    id: int


class UserActionCreateAnswerBase(UserActionBase):
    """Represent base schema for user action that user create an answer."""

    action_type: str = "create_answer"


class UserActionCreateAnswerCreate(UserActionCreateAnswerBase):
    pass


class UserActionCreateAnswerRead(UserActionCreateAnswerBase):
    id: int


class UserActionCreateAnswerCommentBase(UserActionBase):
    """Represent base schema for user action that user create a comment to an answer."""

    action_type: str = "create_answer_comment"


class UserActionCreateAnswerCommentCreate(UserActionCreateAnswerCommentBase):
    pass


class UserActionCreateAnswerCommentRead(UserActionCreateAnswerCommentBase):
    id: int


class UserActionVoteBase(UserActionBase):
    """Represent user action that user vote for something."""

    pass


class UserActionVotePostBase(UserActionVoteBase):
    """Represent base schema for user vote that user vote for post."""

    action_type: str = "vote_post"


class UserActionVotePostCreate(UserActionVotePostBase):
    pass


class UserActionVotePostRead(UserActionVotePostBase):
    id: int


class UserActionVotePostCommentBase(UserActionVoteBase):
    """Represent user action that user vote for a comment in a post."""

    action_type: str = "vote_post_comment"


class UserActionVotePostCommentCreate(UserActionVotePostCommentBase):
    pass


class UserActionVotePostCommentRead(UserActionVotePostCommentBase):
    id: int


class UserActionVotePostBase(UserActionVoteBase):
    """Represent user action that user vote for a question."""

    action_type: str = "vote_question"


class UserActionVoteQuestionCreate(UserActionVotePostBase):
    pass


class UserActionVoteQuestionRead(UserActionVotePostBase):
    id: int


class UserActionVoteAnswerBase(UserActionBase):
    """Represent user action that user vote for an answer."""

    action_type: str = "vote_answer"


class UserActionVoteAnswerCreate(UserActionVoteAnswerBase):
    pass


class UserActionVoteAnswerRead(UserActionVoteAnswerBase):
    id: int


class UserActionReactionBase(UserActionBase):
    """Represent the user action that user react to something."""

    pass


class UserActionReactionPostBase(UserActionReactionBase):
    """Represent the user action that user react to a post."""

    action_type: str = "reaction_post"


class UserActionReactionPostCreate(UserActionReactionPostBase):
    pass


class UserActionReactionPostRead(UserActionReactionPostBase):
    id: int


class UserActionReactionPostCommentBase(UserActionReactionBase):
    """Represent the user action that user react to a comment in a post."""

    action_type: str = "reaction_post_comment"


class UserActionReactionPostCommentCreate(UserActionReactionPostCommentBase):
    pass


class UserActionReactionPostCommentRead(UserActionReactionPostCommentBase):
    id: int


class UserActionReactionQuestionBase(UserActionReactionBase):
    """Represent the user action that user react to a question."""

    action_type: str = "reaction_question"


class UserActionReactionQuestionCreate(UserActionReactionQuestionBase):
    pass


class UserActionReactionQuestionRead(UserActionReactionQuestionBase):
    id: int


class UserActionReactionAnswerBase(UserActionReactionBase):
    """Represent the user action that user react to an answer."""

    action_type: str = "reaction_answer"


class UserActionReactionAnswerCreate(UserActionReactionAnswerBase):
    pass


class UserActionReactionAnswerBase(UserActionReactionAnswerBase):
    id: int


class UserActionReactionAnswerCommentBase(UserActionReactionBase):
    """Represent the user action that user react to a comment in an answer."""

    action_type: str = "reaction_answer_comment"


class UserActionReactionAnswerCommentCreate(UserActionReactionAnswerCommentBase):
    pass


class UserActionReactionAnswerCommentRead(UserActionReactionAnswerCommentBase):
    id: int
