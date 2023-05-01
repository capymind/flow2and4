"""
This is the module for defining schemas related to pyduck community.
"""

from pydantic import Field
from datetime import datetime, timezone
from csduck.pyduck.schemas import PyduckSchema
from csduck.pyduck.auth.schemas import UserRead


class QuestionVoteBase(PyduckSchema):
    """Represent question vote."""

    user_id: int
    question_id: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class QuestionVoteCreate(QuestionVoteBase):
    pass


class QuestionVoteRead(QuestionVoteBase):
    id: int

    # relationship
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

    # relationship
    user: UserRead
    tags: list[QuestionTagRead | None]
    history: list[QuestionHistoryRead | None]
    votes: list[QuestionVoteRead | None]


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
