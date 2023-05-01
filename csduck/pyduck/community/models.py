"""
This is the module for defining ORMs and tables related to pyduck community.
"""

from __future__ import annotations
from sqlalchemy import ForeignKey, Column, Integer
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


class QuestionVote(db.Model):
    """Represent question vote."""

    __bind_key__ = "pyduck"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("user.id"))
    question_id = mapped_column(ForeignKey("question.id"))
    created_at: Mapped[str]

    # relationship
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

    # relationship
    user: Mapped[User] = relationship("pyduck.auth.models.User")
    tags: Mapped[list[QuestionTag]] = relationship(
        secondary=assoc_question_tag_table, back_populates="questions"
    )
    history: Mapped[list[QuestionHistory]] = relationship()
    votes: Mapped[list[QuestionVote]] = relationship()


class QuestionTag(db.Model):
    """Represent question tag."""

    __bind_key__ = "pyduck"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    # relationship
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
