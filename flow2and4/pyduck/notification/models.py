"""
This is the module for defining ORMs and tables related to pyduck notification.

[ models ]
Notification
    NotificationForPostComment
    NotificationForAnswer
    NotificationForAnswerComment
    
    -- about vote.
    NotificationForPostVote
    NotificationForPostCommentVote
    NotificationForQuestionVote
    NotificationForAnswerVote
    
    -- about reaction.
    NotificationForPostReaction
    NotificationForPostCommentReaction
    NotificationForQuestionReaction
    NotificationForAnswerReaction
    NotificationForAnswerCommentReaction
"""

from __future__ import annotations

from sqlalchemy import ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from flow2and4.database import db
from flow2and4.pyduck.auth.models import User
from flow2and4.pyduck.community.models import (
    PostVote,
    Post,
    PostComment,
    PostCommentReaction,
)


class Notification(db.Model):
    """Represent notification."""

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), index=True)
    notification_type: Mapped[str] = mapped_column(index=True)
    notification_value: Mapped[str | None]
    notification_target_id: Mapped[int | None]
    from_user_id = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), nullable=True
    )
    to_user_id = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=True)
    data: Mapped[str | None]
    read: Mapped[bool]
    urgent: Mapped[bool]
    created_at: Mapped[str]
    updated_at: Mapped[str | None]

    __bind_key__ = "pyduck"
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "notification_type",
            "notification_value",
            "notification_target_id",
        ),
        Index(None, "user_id", "notification_type"),
    )
    __mapper_args__ = {
        "polymorphic_on": "notification_type",
        "polymorphic_identity": "notification",
    }

    # relationship
    user: Mapped[User] = relationship("pyduck.auth.models.User", foreign_keys=[user_id])
    from_user: Mapped[User] = relationship(
        "pyduck.auth.models.User", foreign_keys=[from_user_id]
    )


class NotificationForPostComment(Notification):
    """Represent notification that someone create a comment to my post."""

    __mapper_args__ = {"polymorphic_identity": "create_post_comment"}

    # relationship.
    post_comment: Mapped[PostComment] = relationship(
        "PostComment",
        primaryjoin="PostComment.id == foreign(NotificationForPostComment.notification_target_id)",
    )


class NotificationForAnswer(Notification):
    """Represent notification that someone create a answer to my question."""

    __mapper_args__ = {"polymorphic_identity": "create_answer"}


class NotificationForAnswerComment(Notification):
    """Represent notification that someone create a comment to my answer."""

    __mapper_args__ = {"polymorphic_identity": "create_answer_comment"}


# about vote.
class NotificationForPostVote(Notification):
    """Represent notification for voting post."""

    __mapper_args__ = {"polymorphic_identity": "vote_post"}

    # relationship.
    post: Mapped[Post] = relationship(
        "Post",
        primaryjoin="foreign(NotificationForPostVote.notification_target_id) == Post.id",
    )


class NotificationForPostCommentVote(Notification):
    """Represent notification for voting a comment in a post."""

    __mapper_args__ = {"polymorphic_identity": "vote_post_comment"}


class NotificationForQuestionVote(Notification):
    """Represent notification for voting a question."""

    __mapper_args__ = {"polymorphic_identity": "vote_question"}


class NotificationForAnswerVote(Notification):
    """Represent notification for voting an answer."""

    __mapper_args__ = {"polymorphic_identity": "vote_answer"}


# about reaction.
class NotificationForPostReaction(Notification):
    """Represent notification that someone react to my post."""

    __mapper_args__ = {"polymorphic_identity": "reaction_post"}


class NotificationForPostCommentReaction(Notification):
    """Represent notification that someone react to my comment in a post."""

    __mapper_args__ = {"polymorphic_identity": "reaction_post_comment"}

    # relationship.
    post_comment_reaction: Mapped[PostCommentReaction] = relationship(
        "PostCommentReaction",
        primaryjoin="foreign(NotificationForPostCommentReaction.notification_target_id) == PostCommentReaction.id",
    )


class NotificationForQuestionReaction(Notification):
    """Represent notification that someone react to my question."""

    __mapper_args__ = {"polymorphic_identity": "reaction_question"}


class NotificationForAnswerReaction(Notification):
    """Represent notification that someone react to my answer."""

    __mapper_args__ = {"polymorphic_identity": "reaction_answer"}


class NotificationForAnswerCommentReaction(Notification):
    """Represent notification that someone react to my comment in an answer."""

    __mapper_args__ = {"polymorphic_identity": "reaction_answer_comment"}
