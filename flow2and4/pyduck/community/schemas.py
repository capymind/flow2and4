"""
This is the module for defining schemas related to pyduck community.
"""

from datetime import datetime, timezone

from pydantic import Field

from flow2and4.pyduck.auth.schemas import UserRead
from flow2and4.pyduck.schemas import PyduckSchema


class ReactionBase(PyduckSchema):
    """Represent reaction."""

    user_id: int
    target: str
    target_id: int
    code: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class QuestionReactionBase(ReactionBase):
    """Represent reaction to question."""

    target: str = "question"


class QuestionReactionCreate(QuestionReactionBase):
    pass


class QuestionReactionRead(QuestionReactionBase):
    id: int

    # relationship.
    user: UserRead


class AnswerReactionBase(ReactionBase):
    """Represent answer reaction."""

    target: str = "answer"


class AnswerReactionCreate(AnswerReactionBase):
    pass


class AnswerReactionRead(AnswerReactionBase):
    id: int

    # relationship.
    user: UserRead


class AnswerCommentReactionBase(ReactionBase):
    """Represent reaction to comment of answer"""

    target: str = "answer_comment"


class AnswerCommentReactionCreate(AnswerCommentReactionBase):
    pass


class AnswerCommentReactionRead(AnswerCommentReactionBase):
    id: int

    # relationship.
    user: UserRead


class PostReactionBase(ReactionBase):
    """Represent reaction to post."""

    target: str = "post"


class PostReactionCreate(PostReactionBase):
    pass


class PostReactionRead(PostReactionBase):
    id: int

    # relationship.
    user: UserRead


class PostCommentReactionBase(ReactionBase):
    """Represent reaction to comment of post."""

    target: str = "post_comment"


class PostCommentReactionCreate(PostCommentReactionBase):
    pass


class PostCommentReactionRead(PostCommentReactionBase):
    id: int

    # relationship.
    user: UserRead


class VoteBase(PyduckSchema):
    """Represent vote."""

    user_id: int
    target: str
    target_id: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class QuestionVoteBase(VoteBase):
    """Represent vote to question."""

    target: str = "question"


class QuestionVoteCreate(QuestionVoteBase):
    pass


class QuestionVoteRead(QuestionVoteBase):
    id: int

    # relationship.
    user: UserRead


class AnswerVoteBase(VoteBase):
    """Represent vote to answer."""

    target: str = "answer"


class AnswerVoteCreate(AnswerVoteBase):
    pass


class AnswerVoteRead(AnswerVoteBase):
    id: int

    # relationship.
    user: UserRead


class PostVoteBase(VoteBase):
    """Represent vote to post."""

    target: str = "post"


class PostVoteCreate(PostVoteBase):
    pass


class PostVoteRead(PostVoteBase):
    id: int

    # relationship.
    user: UserRead


class PostCommentVoteBase(VoteBase):
    """Represent vote to post's comment."""

    target: str = "post_comment"


class PostCommentVoteCreate(PostCommentVoteBase):
    pass


class PostCommentVoteRead(PostCommentVoteBase):
    id: int

    # relationship


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
    question: QuestionRead
    votes: list[AnswerVoteRead | None]
    reactions: list[AnswerReactionRead | None]


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
    answer: AnswerRead
    history: list[AnswerCommentHistoryRead | None]
    reactions: list[AnswerCommentReactionRead | None]


class PostHistoryBase(PyduckSchema):
    """Represent post history."""

    post_id: int
    title: str
    content: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class PostHistoryCreate(PostHistoryBase):
    pass


class PostHistoryRead(PostHistoryBase):
    id: int


class PostTagBase(PyduckSchema):
    """Represent post tag."""

    name: str


class PostTagCreate(PostTagBase):
    pass


class PostTagRead(PostTagBase):
    id: int


class PostBase(PyduckSchema):
    """Represent post."""

    user_id: int
    category: str
    title: str
    content: str
    view_count: int = 0
    vote_count: int = 0
    comment_count: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime | None
    deleted_at: datetime | None


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    id: int


class PostRead(PostBase):
    id: int

    # relationship.
    user: UserRead
    tags: list[PostTagRead | None]
    history: list[PostHistoryRead | None]
    votes: list[PostVoteRead | None]
    reactions: list[PostReactionRead | None]


class PostImageUploadBase(PyduckSchema):
    """Represent post image upload."""

    user_id: int
    post_id: int | None
    url: str
    filename: str
    original_filename: str
    mimetype: str | None
    filesize: int | None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class PostImageUploadCreate(PostImageUploadBase):
    pass


class PostImageUploadRead(PostImageUploadBase):
    id: int


class PostCommentHistoryBase(PyduckSchema):
    """Represent comment history."""

    comment_id: int
    content: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class PostCommentHistoryCreate(PostCommentHistoryBase):
    pass


class PostCommentHistoryRead(PostCommentHistoryBase):
    id: int


class PostCommentBase(PyduckSchema):
    """Represent comment to post."""

    user_id: int
    post_id: int
    parent_id: int | None
    content: str
    vote_count: int = 0
    comment_count: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime | None
    deleted_at: datetime | None


class PostCommentCreate(PostCommentBase):
    pass


class PostCommentUpdate(PostCommentBase):
    id: int


class PostCommentRead(PostCommentBase):
    id: int

    # relationship.
    user: UserRead
    post: PostRead
    votes: list[PostCommentVoteRead] | None
    history: list[PostCommentHistoryRead] | None
    reactions: list[PostCommentReactionRead] | None
