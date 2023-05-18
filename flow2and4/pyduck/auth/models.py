"""
This is module for defining ORMs and tables related to auth.

[models]
UserAvatar
UserBackdrop
UserSns
User
UserVerificationEmail
UserAction
    UserActionCreatePost
    UserActionCreatePostComment
    UserActionCreateQuestion
    UserActionCreateAnswer
    UserActionCreateAnswerComment
    UserActionVote
        UserActionVotePost
        UserActionVoteQuestion
        UserActionVoteAnswer
        UserActionPostComment
    UserActionReaction
        UserActionReactionPost
        UserActionReactionPostComment
        UserActionReactionQuestion
        UserActionReactionAnswer
        UserActionReactionAnswerComment

"""
from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from flow2and4.database import db
from flow2and4.pyduck.models import ImageUploadMixin

if TYPE_CHECKING:
    from flow2and4.pyduck.community.models import (
        Answer,
        AnswerComment,
        AnswerCommentReaction,
        AnswerReaction,
        Post,
        PostComment,
        PostCommentReaction,
        PostReaction,
        Question,
        QuestionReaction,
        Reaction
    )


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


class UserAction(db.Model):
    """Represent user action."""

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    action_type: Mapped[str] = mapped_column(index=True)
    action_value: Mapped[str | None]
    target_id: Mapped[int | None]
    created_at: Mapped[str]

    __bind_key__ = "pyduck"
    __table_args__ = (
        UniqueConstraint("user_id", "action_type", "action_value", "target_id"),
        Index(None, "user_id", "action_type", "target_id"),
    )
    __mapper_args__ = {
        "polymorphic_on": "action_type",
        "polymorphic_identity": "action",
    }

    # relationship.
    user: Mapped[User] = relationship("pyduck.auth.models.User")


class UserActionCreatePost(UserAction):
    """Represent the action that user create a post."""

    __mapper_args__ = {"polymorphic_identity": "create_post"}

    # relationship.
    post: Mapped[Post] = relationship(
        "Post", primaryjoin="foreign(UserActionCreatePost.target_id) == Post.id"
    )


class UserActionCreatePostComment(UserAction):
    """Represent the action that user create a comment to in post."""

    __mapper_args__ = {"polymorphic_identity": "create_post_comment"}

    # relationship.
    post_comment: Mapped[PostComment] = relationship(
        "PostComment",
        primaryjoin="foreign(UserActionCreatePostComment.target_id) == PostComment.id",
    )


class UserActionCreateQuestion(UserAction):
    """Represent the action that user create a post."""

    __mapper_args__ = {"polymorphic_identity": "create_question"}

    # relationship.
    question: Mapped[Question] = relationship(
        "Question",
        primaryjoin="foreign(UserActionCreateQuestion.target_id) == Question.id",
    )


class UserActionCreateAnswer(UserAction):
    """Represent the action that user create a asnwer to specific question."""

    __mapper_args__ = {"polymorphic_identity": "create_answer"}

    # relationship.
    answer: Mapped[Question] = relationship(
        "Answer",
        primaryjoin="foreign(UserActionCreateAnswer.target_id) == Answer.id",
    )


class UserActionCreateAnswerComment(UserAction):
    """Represent the action that user create a comment to specific answer."""

    __mapper_args__ = {"polymorphic_identity": "create_answer_comment"}

    # relationship.
    answer_comment: Mapped[Question] = relationship(
        "AnswerComment",
        primaryjoin="foreign(UserActionCreateAnswerComment.target_id) == AnswerComment.id",
    )


class UserActionVote(UserAction):
    """Represent the action that user vote for something."""

    __mapper_args__ = {"polymorphic_abstract": True}


class UserActionVotePost(UserActionVote):
    """Represent the action that user vote for Post."""

    __mapper_args__ = {"polymorphic_identity": "vote_post"}

    # relationship.
    post: Mapped[Post] = relationship(
        "Post", primaryjoin="foreign(UserActionVotePost.target_id) == Post.id"
    )


class UserActionVoteQuestion(UserActionVote):
    """Represent the action that user vote for question."""

    __mapper_args__ = {"polymorphic_identity": "vote_question"}

    # relationship.
    question: Mapped[Question] = relationship(
        "Question", primaryjoin="foreign(UserActionVoteQuestion.target_id) == Question.id"
    )


class UserActionVoteAnswer(UserActionVote):
    """Represent the action that user vote for answer."""

    __mapper_args__ = {"polymorphic_identity": "vote_answer"}

    # relationship.
    answer: Mapped[Post] = relationship(
        "Answer", primaryjoin="foreign(UserActionVoteAnswer.target_id) == Answer.id"
    )


class UserActionVotePostComment(UserActionVote):
    """Represent the action that user vote for post comment(1 depth)."""

    __mapper_args__ = {"polymorphic_identity": "vote_post_comment"}

    # relationship.
    post_comment: Mapped[Post] = relationship(
        "PostComment",
        primaryjoin="foreign(UserActionVotePostComment.target_id) == PostComment.id",
    )


class UserActionReaction(UserAction):
    """Represent the action that user react for something."""

    __mapper_args__ = {"polymorphic_abstract": True}


class UserActionReactionPost(UserActionReaction):
    __mapper_args__ = {"polymorphic_identity": "reaction_post"}

    # relationship.
    post: Mapped[Post] = relationship(
        "Post",
        primaryjoin="foreign(UserActionReactionPost.target_id) == Post.id",
        viewonly=True,
    )


class UserActionReactionPostComment(UserActionReaction):
    __mapper_args__ = {"polymorphic_identity": "reaction_post_comment"}

    # relationship.
    post_comment: Mapped[PostComment] = relationship(
        "PostComment",
        primaryjoin="foreign(UserActionReactionPostComment.target_id) == PostComment.id",
        viewonly=True,
    )


class UserActionReactionQuestion(UserActionReaction):
    __mapper_args__ = {"polymorphic_identity": "reaction_question"}

    # relationship.
    question: Mapped[Question] = relationship(
        "Question",
        primaryjoin="foreign(UserActionReactionQuestion.target_id) == Question.id",
        viewonly=True,
    )


class UserActionReactionAnswer(UserActionReaction):
    __mapper_args__ = {"polymorphic_identity": "reaction_answer"}

    # relationship.
    answer: Mapped[Answer] = relationship(
        "Answer",
        primaryjoin="foreign(UserActionReactionAnswer.target_id) == Answer.id",
        viewonly=True,
    )


class UserActionReactionAnswerComment(UserActionReaction):
    __mapper_args__ = {"polymorphic_identity": "reaction_answer_comment"}

    # relationship.
    answer_comment: Mapped[AnswerComment] = relationship(
        "AnswerComment",
        primaryjoin="foreign(UserActionReactionAnswerComment.target_id) == AnswerComment.id",
        viewonly=True,
    )
