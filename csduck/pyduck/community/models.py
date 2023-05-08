"""
This is the module for defining ORMs and tables related to pyduck community.
"""

from __future__ import annotations
from sqlalchemy import ForeignKey, Column, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from csduck.database import db
from csduck.pyduck.models import ImageUploadMixin
from csduck.pyduck.auth.models import User as User


assoc_question_tag_table = db.Table(
    "assoc_question_tag",
    Column("question_id", Integer, ForeignKey("question.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("question_tag.id"), primary_key=True),
    bind_key="pyduck",
)


assoc_post_tag_table = db.Table(
    "assoc_post_tag",
    Column("post_id", Integer, ForeignKey("post.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("post_tag.id", ondelete="CASCADE"), primary_key=True),
    bind_key="pyduck",
)


class QuestionReaction(db.Model):
    """Represent question reaction."""

    __bind_key__ = "pyduck"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("user.id"))
    question_id = mapped_column(ForeignKey("question.id"))
    code: Mapped[str]
    created_at: Mapped[str]

    # constraints.
    __table_args__ = (UniqueConstraint("user_id", "question_id", "code"),)

    # relationship.
    user: Mapped[User] = relationship("pyduck.auth.models.User")


class QuestionVote(db.Model):
    """Represent question vote."""

    __bind_key__ = "pyduck"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("user.id"))
    question_id = mapped_column(ForeignKey("question.id"))
    created_at: Mapped[str]

    # relationship.
    user: Mapped[User] = relationship("pyduck.auth.models.User")


class QuestionHistory(db.Model):
    """Represent question history."""

    __bind_key__ = "pyduck"

    id: Mapped[int] = mapped_column(primary_key=True)
    question_id = mapped_column(ForeignKey("question.id"))
    title: Mapped[str]
    content: Mapped[str]
    created_at: Mapped[str]


class Question(db.Model):
    """Represent question."""

    __bind_key__ = "pyduck"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("user.id"))
    title: Mapped[str]
    content: Mapped[str]
    view_count: Mapped[int]
    vote_count: Mapped[int]
    comment_count: Mapped[int]
    answered: Mapped[bool]
    created_at: Mapped[str]
    updated_at: Mapped[str | None]
    deleted_at: Mapped[str | None]

    # relationship.
    user: Mapped[User] = relationship("pyduck.auth.models.User")
    tags: Mapped[list[QuestionTag]] = relationship(
        secondary=assoc_question_tag_table, back_populates="questions"
    )
    history: Mapped[list[QuestionHistory]] = relationship()
    votes: Mapped[list[QuestionVote]] = relationship()
    reactions: Mapped[list[QuestionReaction]] = relationship()


class QuestionTag(db.Model):
    """Represent question tag."""

    __bind_key__ = "pyduck"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    # relationship.
    questions: Mapped[list[Question]] = relationship(
        secondary=assoc_question_tag_table, back_populates="tags"
    )


class QuestionImageUpload(ImageUploadMixin, db.Model):
    """Represent question image upload."""

    __bind_key__ = "pyduck"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("user.id"))
    question_id = mapped_column(ForeignKey("question.id"))
    created_at: Mapped[str]


class AnswerVote(db.Model):
    """Represent vote to answer."""

    __bind_key__ = "pyduck"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("user.id"))
    answer_id = mapped_column(ForeignKey("answer.id"))
    created_at: Mapped[str]

    # relationship.
    user: Mapped[User] = relationship("pyduck.auth.models.User")


class AnswerReaction(db.Model):
    """Represent reaction to answer."""

    __bind_key__ = "pyduck"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("user.id"))
    answer_id = mapped_column(ForeignKey("answer.id"))
    code: Mapped[str]
    created_at: Mapped[str]

    # relationship.
    user: Mapped[User] = relationship("pyduck.auth.models.User")


class AnswerHistory(db.Model):
    """Represent answer history."""

    __bind_key__ = "pyduck"

    id: Mapped[int] = mapped_column(primary_key=True)
    answer_id = mapped_column(ForeignKey("answer.id"))
    content: Mapped[str]
    created_at: Mapped[str]


class Answer(db.Model):
    """Represent answer to question."""

    __bind_key__ = "pyduck"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("user.id"))
    question_id = mapped_column(ForeignKey("question.id"))
    content: Mapped[str]
    vote_count: Mapped[int]
    comment_count: Mapped[int]
    answered: Mapped[bool]
    created_at: Mapped[str]
    updated_at: Mapped[str | None]
    deleted_at: Mapped[str | None]

    # relationship.
    user: Mapped[User] = relationship("pyduck.auth.models.User")
    history: Mapped[list[AnswerHistory]] = relationship()
    question: Mapped[Question] = relationship()
    votes: Mapped[list[AnswerVote]] = relationship()
    reactions: Mapped[list[AnswerReaction]] = relationship()


class AnswerComment(db.Model):
    """Represent comment to answer of question."""

    __bind_key__ = "pyduck"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("user.id"))
    answer_id = mapped_column(ForeignKey("answer.id"))
    content: Mapped[str]
    created_at: Mapped[str]
    updated_at: Mapped[str | None]
    deleted_at: Mapped[str | None]

    # relationship.
    user: Mapped[User] = relationship("pyduck.auth.models.User")
    history: Mapped[list[AnswerCommentHistory]] = relationship()
    reactions: Mapped[list[AnswerCommentReaction]] = relationship()


class AnswerCommentReaction(db.Model):
    """Represent reaction to comment to answer of question."""

    __bind_key__ = "pyduck"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("user.id"))
    comment_id = mapped_column(ForeignKey("answer_comment.id"))
    code: Mapped[str]
    created_at: Mapped[str]

    # relationship.
    user: Mapped[User] = relationship("pyduck.auth.models.User")


class AnswerCommentHistory(db.Model):
    """Represent history of comment to answer of question."""

    __bind_key__ = "pyduck"

    id: Mapped[int] = mapped_column(primary_key=True)
    comment_id = mapped_column(ForeignKey("answer_comment.id"))
    content: Mapped[str]
    created_at: Mapped[str]


class PostReaction(db.Model):
    """Represent post reaction."""

    __bind_key__ = "pyduck"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("user.id"))
    post_id = mapped_column(ForeignKey("post.id"))
    code: Mapped[str]
    created_at: Mapped[str]

    # constraints.
    __table_args__ = (UniqueConstraint("user_id", "post_id", "code"),)

    # relationship.
    user: Mapped[User] = relationship("pyduck.auth.models.User")


class PostVote(db.Model):
    """Represent post vote."""

    __bind_key__ = "pyduck"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("user.id"))
    post_id = mapped_column(ForeignKey("post.id"))
    created_at: Mapped[str]

    # relationship.
    user: Mapped[User] = relationship("pyduck.auth.models.User")


class PostHistory(db.Model):
    """Represent post history."""

    __bind_key__ = "pyduck"

    id: Mapped[int] = mapped_column(primary_key=True)
    post_id = mapped_column(ForeignKey("post.id"))
    title: Mapped[str]
    content: Mapped[str]
    created_at: Mapped[str]


class Post(db.Model):
    """Represent post."""

    __bind_key__ = "pyduck"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("user.id"))
    category: Mapped[str] = mapped_column(index=True)
    title: Mapped[str]
    content: Mapped[str]
    view_count: Mapped[int]
    vote_count: Mapped[int]
    comment_count: Mapped[int]
    created_at: Mapped[str]
    updated_at: Mapped[str | None]
    deleted_at: Mapped[str | None]

    # relationship.
    user: Mapped[User] = relationship("pyduck.auth.models.User")
    tags: Mapped[list[PostTag]] = relationship(
        secondary=assoc_post_tag_table, back_populates="posts"
    )
    history: Mapped[list[PostHistory]] = relationship()
    votes: Mapped[list[PostVote]] = relationship()
    reactions: Mapped[list[PostReaction]] = relationship()


class PostTag(db.Model):
    """Represent post tag."""

    __bind_key__ = "pyduck"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    # relationship.
    posts: Mapped[list[Post]] = relationship(
        secondary=assoc_post_tag_table, back_populates="tags"
    )


class PostImageUpload(ImageUploadMixin, db.Model):
    """Represent post image upload."""

    __bind_key__ = "pyduck"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("user.id"))
    post_id = mapped_column(ForeignKey("post.id"))
    created_at: Mapped[str]


class PostCommentVote(db.Model):
    """Represent a vote to a comment of a post."""

    __bind_key__ = "pyduck"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("user.id"))
    comment_id = mapped_column(ForeignKey("post_comment.id"))
    created_at: Mapped[str]

class PostCommentReaction(db.Model):
    """Represent a reaction to a comment of a post."""

    __bind_key__ = "pyduck"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("user.id"))
    comment_id = mapped_column(ForeignKey("post_comment.id"))
    code: Mapped[str]
    created_at: Mapped[str]

    # relationship.
    user: Mapped[User] = relationship("pyduck.auth.models.User")


class PostCommentHistory(db.Model):
    """Represent history of a comment to a post."""

    __bind_key__ = "pyduck"

    id: Mapped[int] = mapped_column(primary_key=True)
    comment_id = mapped_column(ForeignKey("post_comment.id"))
    content: Mapped[str]
    created_at: Mapped[str]


class PostComment(db.Model):
    """Represent comment to post."""

    __bind_key__ = "pyduck"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("user.id"))
    post_id = mapped_column(ForeignKey("post.id"))
    parent_id = mapped_column(ForeignKey("post_comment.id"))
    content: Mapped[str]
    vote_count: Mapped[int]
    comment_count: Mapped[int]
    created_at: Mapped[str]
    updated_at: Mapped[str | None]
    deleted_at: Mapped[str | None]

    # relationship.
    user: Mapped[User] = relationship("pyduck.auth.models.User")
    history: Mapped[list[PostCommentHistory]] = relationship()
    votes: Mapped[list[PostCommentVote]] = relationship()
    reactions: Mapped[list[PostCommentReaction]] = relationship()
