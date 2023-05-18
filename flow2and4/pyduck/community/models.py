"""
This is the module for defining ORMs and tables related to pyduck community.

[models]

Vote
    QuestionVote
    AnswerReaction
    PostVote
    PostCommentVote
Reaction
    QuestionReaction
    AnswerReaction
    AnswerCommentReaction
    PostReaction
    PostCommentReaction
"""

from __future__ import annotations

from sqlalchemy import Column, ForeignKey, Index, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, foreign, mapped_column, relationship, remote

from flow2and4.database import db
from flow2and4.pyduck.auth.models import User as User
from flow2and4.pyduck.models import ImageUploadMixin

assoc_question_tag_table = db.Table(
    "assoc_question_tag",
    Column("question_id", Integer, ForeignKey("question.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("question_tag.id"), primary_key=True),
    bind_key="pyduck",
)


assoc_post_tag_table = db.Table(
    "assoc_post_tag",
    Column(
        "post_id", Integer, ForeignKey("post.id", ondelete="CASCADE"), primary_key=True
    ),
    Column(
        "tag_id",
        Integer,
        ForeignKey("post_tag.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    bind_key="pyduck",
)


class Vote(db.Model):
    """Represent vote."""

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("user.id"), index=True)
    target: Mapped[str] = mapped_column(index=True)
    target_id: Mapped[int]
    created_at: Mapped[str]

    # configuration.
    __bind_key__ = "pyduck"
    __table_args__ = (
        UniqueConstraint("user_id", "target", "target_id"),
        Index("target", "target_id"),
    )
    __mapper_args__ = {"polymorphic_on": "target", "polymorphic_identity": "vote"}

    # relationship.
    user: Mapped[User] = relationship("pyduck.auth.models.User")


class QuestionVote(Vote):
    """Represent vote to question."""

    __mapper_args__ = {"polymorphic_identity": "question"}

    # relationship.
    question: Mapped[Question] = relationship(
        "Question",
        primaryjoin="foreign(QuestionVote.target_id) == Question.id",
    )


class AnswerVote(Vote):
    """Represent vote to answer."""

    __mapper_args__ = {"polymorphic_identity": "answer"}

    # relationship.
    answer: Mapped[Answer] = relationship(
        "Answer",
        primaryjoin="foreign(AnswerVote.target_id) == Answer.id",
    )


class PostVote(Vote):
    """Represent vote to post."""

    __mapper_args__ = {"polymorphic_identity": "post"}
    # relationship.
    post: Mapped[Post] = relationship(
        "Post", primaryjoin="foreign(PostVote.target_id) == Post.id"
    )


class PostCommentVote(Vote):
    """Represent vote to post's comment."""

    __mapper_args__ = {"polymorphic_identity": "post_comment"}

    # relationship.
    post_comment: Mapped[PostComment] = relationship(
        "PostComment",
        primaryjoin="foreign(PostCommentVote.target_id) == PostComment.id",
    )


class Reaction(db.Model):
    """Represent reaction."""

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("user.id"), index=True)
    target: Mapped[str] = mapped_column(index=True)
    target_id: Mapped[int]
    code: Mapped[str]
    created_at: Mapped[str]

    # configuration.
    __bind_key__ = "pyduck"
    __table_args__ = (UniqueConstraint("user_id", "target", "target_id", "code"),)
    __mapper_args__ = {"polymorphic_on": "target", "polymorphic_identity": "reaction"}

    # relationship.
    user: Mapped[User] = relationship("pyduck.auth.models.User")


class QuestionReaction(Reaction):
    """Represent reaction to questionn."""

    __mapper_args__ = {"polymorphic_identity": "question"}

    # relationship.
    question: Mapped[Question] = relationship(
        "Question",
        primaryjoin="foreign(QuestionReaction.target_id) == Question.id",
    )


class AnswerReaction(Reaction):
    """Represent reaction to answer."""

    __mapper_args__ = {"polymorphic_identity": "answer"}

    # relationship.
    answer: Mapped[Answer] = relationship(
        "Answer",
        primaryjoin="foreign(AnswerReaction.target_id) == Answer.id",
    )


class AnswerCommentReaction(Reaction):
    """Represent reaction to comment to answer of question."""

    __mapper_args__ = {"polymorphic_identity": "answer_comment"}

    # relationship.
    answer_comment: Mapped[AnswerComment] = relationship(
        "AnswerComment",
        primaryjoin="foreign(AnswerCommentReaction.target_id) == AnswerComment.id",
    )


class PostReaction(Reaction):
    """Represent reaction to post."""

    __mapper_args__ = {"polymorphic_identity": "post"}

    # relationship.
    post: Mapped[Post] = relationship(
        "Post",
        primaryjoin="foreign(PostReaction.target_id) == Post.id",
    )


class PostCommentReaction(Reaction):
    """Represent reaction to comment of post."""

    __mapper_args__ = {"polymorphic_identity": "post_comment"}

    # relationship.
    post_comment: Mapped[PostComment] = relationship(
        "PostComment",
        primaryjoin="foreign(PostCommentReaction.target_id) == PostComment.id",
    )


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
    votes: Mapped[list[QuestionVote]] = relationship(
        "QuestionVote", primaryjoin="Question.id == foreign(QuestionVote.target_id)"
    )
    reactions: Mapped[list[QuestionReaction]] = relationship(
        "QuestionReaction",
        primaryjoin="Question.id == foreign(QuestionReaction.target_id)",
    )


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
    votes: Mapped[list[AnswerVote]] = relationship(
        "AnswerVote", primaryjoin="Answer.id == foreign(AnswerVote.target_id)"
    )
    reactions: Mapped[list[AnswerReaction]] = relationship(
        "AnswerReaction", primaryjoin="Answer.id == foreign(AnswerReaction.target_id)"
    )


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
    answer: Mapped[Answer] = relationship()
    history: Mapped[list[AnswerCommentHistory]] = relationship()
    reactions: Mapped[list[AnswerCommentReaction]] = relationship(
        "AnswerCommentReaction",
        primaryjoin="AnswerComment.id == foreign(AnswerCommentReaction.target_id)",
    )


class AnswerCommentHistory(db.Model):
    """Represent history of comment to answer of question."""

    __bind_key__ = "pyduck"

    id: Mapped[int] = mapped_column(primary_key=True)
    comment_id = mapped_column(ForeignKey("answer_comment.id"))
    content: Mapped[str]
    created_at: Mapped[str]


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
    votes: Mapped[list[PostVote]] = relationship(
        "PostVote", primaryjoin="Post.id == foreign(PostVote.target_id)"
    )
    reactions: Mapped[list[PostReaction]] = relationship(
        "PostReaction", primaryjoin="Post.id == foreign(PostReaction.target_id)"
    )


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
    post_id = mapped_column(ForeignKey("post.id"), nullable=False)
    parent_id = mapped_column(ForeignKey("post_comment.id"))
    content: Mapped[str]
    vote_count: Mapped[int]
    comment_count: Mapped[int]
    created_at: Mapped[str]
    updated_at: Mapped[str | None]
    deleted_at: Mapped[str | None]

    # relationship.
    user: Mapped[User] = relationship("pyduck.auth.models.User")
    post: Mapped[Post] = relationship()
    history: Mapped[list[PostCommentHistory]] = relationship()
    votes: Mapped[list[PostCommentVote]] = relationship(
        "PostCommentVote",
        primaryjoin="PostComment.id == foreign(PostCommentVote.target_id)",
    )
    reactions: Mapped[list[PostCommentReaction]] = relationship(
        "PostCommentReaction",
        primaryjoin="PostComment.id == foreign(PostCommentReaction.target_id)",
    )
