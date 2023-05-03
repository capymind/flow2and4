"""
This is the module for defining schemas related to pyduck community.
"""

from pydantic import Field
from datetime import datetime, timezone
from csduck.pyduck.schemas import PyduckSchema
from csduck.pyduck.auth.schemas import UserRead


class QuestionReactionBase(PyduckSchema):
    """Represent question reaction."""

    user_id: int
    question_id: int
    code: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class QuestionReactionCreate(QuestionReactionBase):
    pass


class QuestionReactionRead(QuestionReactionBase):
    id: int

    # relationship.
    user: UserRead


class QuestionVoteBase(PyduckSchema):
    """Represent question vote."""

    user_id: int
    question_id: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class QuestionVoteCreate(QuestionVoteBase):
    pass


class QuestionVoteRead(QuestionVoteBase):
    id: int

    # relationship.
    user: UserRead


class QuestionHistoryBase(PyduckSchema):
    """Represent question history."""

    question_id: int
    title: str
    content: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class QuestionHistoryCreate(QuestionHistoryBase):
    pass


class QuestionHistoryRead(QuestionHistoryBase):
    id: int


class QuestionTagBase(PyduckSchema):
    """Represent question tag."""

    name: str


class QuestionTagCreate(QuestionTagBase):
    pass


class QuestionTagRead(QuestionTagBase):
    id: int


class QuestionBase(PyduckSchema):
    """Represent question."""

    user_id: int
    title: str
    content: str
    view_count: int = 0
    vote_count: int = 0
    comment_count: int = 0
    answered: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime | None
    deleted_at: datetime | None


class QuestionCreate(QuestionBase):
    pass


class QuestionUpdate(QuestionBase):
    id: int


class QuestionRead(QuestionBase):
    id: int

    # relationship.
    user: UserRead
    tags: list[QuestionTagRead | None]
    history: list[QuestionHistoryRead | None]
    votes: list[QuestionVoteRead | None]
    reactions: list[QuestionReactionRead | None]


class QuestionImageUploadBase(PyduckSchema):
    """Represent question image upload."""

    user_id: int
    question_id: int | None
    url: str
    filename: str
    original_filename: str
    mimetype: str | None
    filesize: int | None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class QuestionImageUploadCreate(QuestionImageUploadBase):
    pass


class QuestionImageUploadRead(QuestionImageUploadBase):
    id: int


class AnswerReactionBase(PyduckSchema):
    """Represent answer reaction."""

    user_id: int
    answer_id: int
    code: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AnswerReactionCreate(AnswerReactionBase):
    pass


class AnswerReactionRead(AnswerReactionBase):
    id: int

    # relationship.
    user: UserRead


class AnswerVoteBase(PyduckSchema):
    """Represent question vote."""

    user_id: int
    answer_id: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AnswerVoteCreate(AnswerVoteBase):
    pass


class AnswerVoteRead(AnswerVoteBase):
    id: int

    # relationship.
    user: UserRead


class AnswerHistoryBase(PyduckSchema):
    """Represent question history."""

    answer_id: int
    content: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AnswerHistoryCreate(AnswerHistoryBase):
    pass


class AnswerHistoryRead(AnswerHistoryBase):
    id: int


class AnswerBase(PyduckSchema):
    """Represent answer (to question)."""

    user_id: int
    question_id: int
    content: str
    vote_count: int = 0
    comment_count: int = 0
    answered: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime | None
    deleted_at: datetime | None


class AnswerCreate(AnswerBase):
    pass


class AnswerUpdate(AnswerBase):
    id: int


class AnswerRead(AnswerBase):
    id: int

    # relationship.
    user: UserRead
    history: list[AnswerHistoryRead | None]
    votes: list[AnswerVoteRead | None]
    reactions: list[AnswerReactionRead | None]


class AnswerCommentReactionBase(PyduckSchema):
    """Represent answer reaction."""

    user_id: int
    comment_id: int
    code: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AnswerCommentReactionCreate(AnswerCommentReactionBase):
    pass


class AnswerCommentReactionRead(AnswerCommentReactionBase):
    id: int

    # relationship.
    user: UserRead


class AnswerCommentHistoryBase(PyduckSchema):
    """Represent comment history."""

    comment_id: int
    content: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AnswerCommentHistoryCreate(AnswerCommentHistoryBase):
    pass


class AnswerCommentHistoryRead(AnswerCommentHistoryBase):
    id: int


class AnswerCommentBase(PyduckSchema):
    """Represent comment to answer of question."""

    user_id: int
    answer_id: int
    content: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime | None
    deleted_at: datetime | None


class AnswerCommentCreate(AnswerCommentBase):
    pass


class AnswerCommentUpdate(AnswerCommentBase):
    id: int


class AnswerCommentRead(AnswerCommentBase):
    id: int

    # relationship.
    user: UserRead
    history: list[AnswerCommentHistoryRead | None]
    reactions: list[AnswerCommentReactionRead | None]
