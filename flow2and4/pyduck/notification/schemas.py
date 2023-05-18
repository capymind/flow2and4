"""
This is the module for defining schemas related to pyduck notification.

[schemas]

NotificationBase

    -- about vote.
    NotificationForPostVoteBase
        NotificationForPostVoteCreate
        NotificationForPostVoteReade
    NotificationForPostCommentVoteBase
        NotificationForPostCommentVoteCreate
        NotificationForPostCommentVoteRead
    NotificationForQuestionVoteBase
        NotificationForQuestionVoteCreate
        NotificationForQuestionVoteRead
    NotificationForAnswerVoteBase
        NotificationForAnswerVoteCreate
        NotificationForAnswerVoteRead

    -- about reaction.
    NotificationForPostReactionBase
        NotificationForPostReactionCreate
        NotificationForPostReactionRead
    NotificationForPostCommentReactionBase
        NotificationForPostCommentReactionCreate
        NotificationForPostCommentReactionRead
    NotificationForQuestionReactionBase
        NotificationForQuestionReactionCreate
        NotificationForQuestionReactionRead
    NotificationForAnswerReactionBase
        NotificationForAnswerReactionCreate
        NotificationForAnswerReactionRead
    NotificationForAnswerCommentReactionBase
        NotificationForAnswerCommentReactionCreate
        NotificationForAnswerCommentReactionRead
"""

from datetime import datetime, timezone

from pydantic import Field

from flow2and4.pyduck.schemas import PyduckSchema


class NotificationBase(PyduckSchema):
    """Represent notification base schema."""

    user_id: int
    notification_type: str
    notification_value: str | None
    notification_target_id: int | None
    from_user_id: int | None
    to_user_id: int | None
    data: str | None
    read: bool | None = False
    urgent: bool | None = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime | None


class NotificationForPostCommentBase(NotificationBase):
    """Represent notification that someone comment in my post."""

    notification_type: str = "create_post_comment"


class NotificationForPostCommentCreate(NotificationForPostCommentBase):
    pass


class NotificationForPostCommentRead(NotificationForPostCommentBase):
    id: int


class NotificationForAnswerBase(NotificationBase):
    """Represent notification that someone answer to my question."""

    notification_type: str = "create_answer"


class NotificationForAnswerCreate(NotificationForAnswerBase):
    pass


class NotificationForAnswerRead(NotificationForAnswerBase):
    id: int


class NotificationForAnswerCommentBase(NotificationBase):
    """Represent notification that someone comment to my answer."""

    notification_type: str = "create_answer_comment"


class NotificationForAnswerCommentCreate(NotificationForAnswerCommentBase):
    pass


class NotificationForAnswerCommentRead(NotificationForAnswerCommentBase):
    id: int


# about vote.
class NotificationForPostVoteBase(NotificationBase):
    """Represent notification that someone vote for my post."""

    notification_type: str = "vote_post"


class NotificationForPostVoteCreate(NotificationForPostVoteBase):
    pass


class NotificationForPostVoteRead(NotificationForPostVoteBase):
    id: int


class NotificationForPostCommentVoteBase(NotificationBase):
    """Represent notification that someone vote for my comment in post."""

    notification_type: str = "vote_post_comment"


class NotificationForPostCommentVoteCreate(NotificationForPostCommentVoteBase):
    pass


class NotificationForPostCommentVoteRead(NotificationForPostCommentVoteBase):
    id: int


class NotificationForQuestionVoteBase(NotificationBase):
    """Represent notification that someone vote for my question."""

    notification_type: str = "vote_question"


class NotificationForQuestionVoteCreate(NotificationForQuestionVoteBase):
    pass


class NotificationForQuestionVoteRead(NotificationForQuestionVoteBase):
    id: int


class NotificationForAnswerVoteBase(NotificationBase):
    """Represent notification that someone vote for my post."""

    notification_type: str = "vote_answer"


class NotificationForAnswerVoteCreate(NotificationForAnswerVoteBase):
    pass


class NotificationForAnswerVoteRead(NotificationForAnswerVoteBase):
    id: int


# about reaction.
class NotificationForPostReactionBase(NotificationBase):
    """Represent notification that someone react to my post."""

    notification_type: str = "reaction_post"


class NotificationForPostReactionCreate(NotificationForPostReactionBase):
    pass


class NotificationForPostReactionRead(NotificationForPostReactionBase):
    id: int


class NotificationForPostReactionBase(NotificationBase):
    """Represent notification that someone react to my post."""

    notification_type: str = "reaction_post"


class NotificationForPostReactionCreate(NotificationForPostReactionBase):
    pass


class NotificationForPostReactionRead(NotificationForPostReactionBase):
    id: int


class NotificationForPostCommentReactionBase(NotificationBase):
    """Represent notification that someone react to my comment in a post."""

    notification_type: str = "reaction_post_comment"


class NotificationForPostCommentReactionCreate(NotificationForPostCommentReactionBase):
    pass


class NotificationForPostCommentReactionRead(NotificationForPostCommentReactionBase):
    id: int


class NotificationForQuestionReactionBase(NotificationBase):
    """Represent notification that someone react to my question."""

    notification_type: str = "reaction_question"


class NotificationForQuestionReactionCreate(NotificationForQuestionReactionBase):
    pass


class NotificationForQuestionReactionRead(NotificationForQuestionReactionBase):
    id: int


class NotificationForAnswerReactionBase(NotificationBase):
    """Represent notification that someone react to my answer."""

    notification_type: str = "reaction_answer"


class NotificationForAnswerReactionCreate(NotificationForAnswerReactionBase):
    pass


class NotificationForAnswerReactionRead(NotificationForAnswerReactionBase):
    id: int


class NotificationForAnswerCommentReactionBase(NotificationBase):
    """Represent notification that someone react to my comment in an answer."""

    notification_type: str = "reaction_answer_comment"


class NotificationForAnswerCommentReactionCreate(
    NotificationForAnswerCommentReactionBase
):
    pass


class NotificationForAnswerCommentReactionRead(
    NotificationForAnswerCommentReactionBase
):
    id: int
