"""
This is the module for handling database transactions related to pyduck community.
"""

from csduck.database import db
from csduck.pyduck.community.schemas import (
    QuestionImageUploadCreate,
    QuestionImageUploadRead,
    QuestionCreate,
    QuestionRead,
    QuestionUpdate,
    QuestionTagCreate,
    QuestionTagRead,
    QuestionHistoryCreate,
    QuestionVoteCreate,
    QuestionVoteRead,
    QuestionReactionCreate,
    QuestionReactionRead,
    AnswerCreate,
    AnswerRead,
    AnswerUpdate,
    AnswerHistoryCreate,
    AnswerVoteCreate,
    AnswerVoteRead,
    AnswerReactionCreate,
    AnswerReactionRead,
    AnswerCommentCreate,
    AnswerCommentRead,
    AnswerCommentUpdate,
    AnswerCommentHistoryCreate,
    AnswerCommentReactionCreate,
    AnswerCommentReactionRead,
)
from csduck.pyduck.community.models import (
    QuestionImageUpload,
    Question,
    QuestionTag,
    QuestionHistory,
    QuestionVote,
    QuestionReaction,
    Answer,
    AnswerHistory,
    AnswerVote,
    AnswerReaction,
    AnswerComment,
    AnswerCommentHistory,
    AnswerCommentReaction,
)
from sqlalchemy import select
from flask_sqlalchemy.pagination import Pagination


def create_question_image_upload(
    *, upload_in: QuestionImageUploadCreate
) -> QuestionImageUploadRead:
    """Insert question image upload in table."""

    upload = QuestionImageUpload(**upload_in.dict())
    db.session.add(upload)
    db.session.commit()

    return QuestionImageUploadRead.from_orm(upload)


def create_question(
    *, question_in: QuestionCreate, tags_in: list[QuestionTag]
) -> QuestionRead:
    """Insert question in table."""

    question = Question(**question_in.dict())
    for tag_in in tags_in:
        question.tags.append(tag_in)
    db.session.add(question)
    db.session.commit()

    return QuestionRead.from_orm(question)


def _get_tag_by_name(name: str) -> QuestionTag | None:
    """Select tag by name."""

    return db.session.scalars(select(QuestionTag).filter_by(name=name)).one_or_none()


def _create_tag_by_name(name: str) -> QuestionTagRead:
    """Create tag by name."""

    tag = QuestionTag(name=name)
    db.session.add(tag)
    db.session.commit()

    return tag


def get_or_create_tags(*, tags_in: list[str]) -> list[QuestionTagRead]:
    """Select tags (Create if tags doesn't exist)."""

    tags = []
    for name in tags_in:
        tag = _get_tag_by_name(name)

        if tag is not None:
            tags.append(tag)
        else:
            tags.append(_create_tag_by_name(name))
    return tags


def get_all_questions_by_commons(
    *, page, per_page, max_per_page, filters, sorters, query: str
) -> Pagination:
    """Select all posts by common parameters.

    TODO
    : very limited form and functionality of search-filter-sorter...
    """
    model = Question
    select_ = select(model)

    # handle searching.
    if query is not None:
        field, _, value = query.split("-", maxsplit=2)
        where_ = getattr(model, field).contains(value)
        select_ = select_.where(where_)

    # handle filtering.
    _filters = []
    for filter_ in filters:
        field, f, value = filter_.split("-")
        column = getattr(model, field)
        if f == "eq":
            _filters.append(column == value)
    select_ = select_.where(*_filters)

    # handle sorting.
    _sorters = []
    for sorter in sorters:
        field, direction = sorter.split("-")
        column = getattr(model, field)
        _sorters.append(column.asc() if direction == "asc" else column.desc())

    _sorters.append(model.created_at.desc())  # default sorting.
    select_ = select_.order_by(*_sorters)

    # handle paginating and return.
    return db.paginate(select_, page=page, per_page=per_page, max_per_page=max_per_page)


def _get_question(id: int) -> Question | None:
    return db.session.scalars(select(Question).filter_by(id=id)).one_or_none()


def get_question(*, question_id: int) -> QuestionRead | None:
    """Select question."""

    question = _get_question(question_id)

    return QuestionRead.from_orm(question) if question is not None else None


def update_question_adding_history(
    *, question_in: QuestionUpdate, tags_in: list[QuestionTag | None]
) -> QuestionRead:
    """Update question, insert question history in table."""

    question = _get_question(question_in.id)

    history_in = QuestionHistoryCreate(
        question_id=question.id, title=question.title, content=question.content
    )
    history = QuestionHistory(**history_in.dict())

    updated_data = question_in.dict(include={"title", "content", "updated_at"})

    for column, value in updated_data.items():
        setattr(question, column, value)

    question.tags.clear()
    for tag_in in tags_in:
        question.tags.append(tag_in)

    db.session.add(history)
    db.session.commit()

    return QuestionRead.from_orm(question)


def create_question_vote(vote_in: QuestionVoteCreate) -> QuestionRead:
    """Insert question vote in table."""

    question = _get_question(id=vote_in.question_id)
    question.vote_count += 1

    vote = QuestionVote(**vote_in.dict())
    db.session.add(vote)
    db.session.commit()

    return QuestionRead.from_orm(question)


def get_question_vote(*, question_id: int, user_id: int) -> QuestionVote:
    """Select question vote."""

    return db.session.scalars(
        select(QuestionVote).filter_by(question_id=question_id, user_id=user_id)
    ).one_or_none()


def delete_question_vote(*, question_id: int, user_id: int) -> QuestionRead:
    """Delete question vote and return relevant question."""

    question = _get_question(id=question_id)
    question.vote_count -= 1

    vote = get_question_vote(question_id=question_id, user_id=user_id)
    db.session.delete(vote)
    db.session.commit()

    return QuestionRead.from_orm(question)


def create_question_reaction(*, reaction_in: QuestionReactionCreate) -> QuestionRead:
    """Insert question reaction in table and return relevant question."""

    question = _get_question(id=reaction_in.question_id)

    reaction = QuestionReaction(**reaction_in.dict())
    db.session.add(reaction)
    db.session.commit()

    return QuestionRead.from_orm(question)


def get_question_reaction(
    *, question_id: int, user_id: int, code: str
) -> QuestionReaction | None:
    """Select question reaction."""

    return db.session.scalars(
        select(QuestionReaction).filter_by(
            question_id=question_id, user_id=user_id, code=code
        )
    ).one_or_none()


def delete_question_reaction(
    *, question_id: int, user_id: int, code: str
) -> QuestionRead:
    """Delete question reaction and return relevant question."""

    reaction = get_question_reaction(
        question_id=question_id, user_id=user_id, code=code
    )
    db.session.delete(reaction)
    db.session.commit()

    question = get_question(question_id=question_id)
    return QuestionRead.from_orm(question)


def create_answer(*, answer_in: AnswerCreate) -> AnswerRead:
    """Insert answer in table."""

    answer = Answer(**answer_in.dict())
    db.session.add(answer)

    question = _get_question(answer.question_id)
    question.comment_count += 1

    db.session.commit()

    return AnswerRead.from_orm(answer)


def _get_answer(id: int) -> Answer | None:
    return db.session.scalars(select(Answer).filter_by(id=id)).one_or_none()


def get_answer(*, answer_id: int) -> AnswerRead | None:
    """Select question."""

    answer = _get_answer(answer_id)

    return AnswerRead.from_orm(answer) if answer is not None else None


def create_answer_vote(vote_in: AnswerVoteCreate) -> AnswerRead:
    """Insert answer vote and return relevant answer."""

    answer = _get_answer(id=vote_in.answer_id)
    answer.vote_count += 1

    vote = AnswerVote(**vote_in.dict())
    db.session.add(vote)
    db.session.commit()

    return AnswerRead.from_orm(answer)


def get_answer_vote(*, answer_id: int, user_id: int) -> AnswerVote:
    """Select answer vote."""

    return db.session.scalars(
        select(AnswerVote).filter_by(answer_id=answer_id, user_id=user_id)
    ).one_or_none()


def delete_answer_vote(*, answer_id: int, user_id: int) -> AnswerRead:
    """Delete answer vote and return relevant answer."""

    answer = _get_answer(id=answer_id)
    answer.vote_count -= 1

    vote = get_answer_vote(answer_id=answer_id, user_id=user_id)
    db.session.delete(vote)
    db.session.commit()

    return AnswerRead.from_orm(answer)


def create_answer_reaction(*, reaction_in: AnswerReactionCreate) -> AnswerRead:
    """Insert answer reaction in table and return relevant answer."""

    answer = _get_answer(id=reaction_in.answer_id)

    reaction = AnswerReaction(**reaction_in.dict())
    db.session.add(reaction)
    db.session.commit()

    return AnswerRead.from_orm(answer)


def get_answer_reaction(
    *, answer_id: int, user_id: int, code: str
) -> AnswerReaction | None:
    """Select answer reaction."""

    return db.session.scalars(
        select(AnswerReaction).filter_by(
            answer_id=answer_id, user_id=user_id, code=code
        )
    ).one_or_none()


def delete_answer_reaction(*, answer_id: int, user_id: int, code: str) -> AnswerRead:
    """Delete answer reaction and return relevant question."""

    reaction = get_answer_reaction(answer_id=answer_id, user_id=user_id, code=code)
    db.session.delete(reaction)
    db.session.commit()

    answer = get_answer(answer_id=answer_id)
    return AnswerRead.from_orm(answer)


def get_all_answers_by_commons(
    *, page, per_page, max_per_page, filters, sorters, query: str, question_id: int
) -> Pagination:
    """Select all answers by common parameters.

    TODO
    : very limited form and functionality of search-filter-sorter...
    """
    model = Answer
    select_ = select(model).filter_by(question_id=question_id)

    # handle searching.
    if query is not None:
        field, _, value = query.split("-", maxsplit=2)
        where_ = getattr(model, field).contains(value)
        select_ = select_.where(where_)

    # handle filtering.
    _filters = []
    for filter_ in filters:
        field, f, value = filter_.split("-")
        column = getattr(model, field)
        if f == "eq":
            _filters.append(column == value)
    select_ = select_.where(*_filters)

    # handle sorting.
    _sorters = []
    for sorter in sorters:
        field, direction = sorter.split("-")
        column = getattr(model, field)
        _sorters.append(column.asc() if direction == "asc" else column.desc())

    _sorters.append(model.created_at.desc())  # default sorting.
    select_ = select_.order_by(*_sorters)

    # handle paginating and return.
    return db.paginate(select_, page=page, per_page=per_page, max_per_page=max_per_page)


def update_answer_adding_history(*, answer_in: AnswerUpdate) -> AnswerRead:
    """Update question, insert question history in table."""

    answer = _get_answer(answer_in.id)

    history_in = AnswerHistoryCreate(answer_id=answer.id, content=answer.content)
    history = AnswerHistory(**history_in.dict())
    db.session.add(history)

    updated_data = answer_in.dict(include={"content", "updated_at"})
    for column, value in updated_data.items():
        setattr(answer, column, value)

    db.session.commit()

    return AnswerRead.from_orm(answer)


def create_answer_comment(*, comment_in: AnswerCommentCreate) -> AnswerCommentRead:
    """Insert answer's comment in table."""

    comment = AnswerComment(**comment_in.dict())
    db.session.add(comment)

    answer = _get_answer(comment.answer_id)
    answer.comment_count += 1

    db.session.commit()

    return AnswerCommentRead.from_orm(comment)


def _get_comment(id: int) -> AnswerComment | None:
    return db.session.scalars(select(AnswerComment).filter_by(id=id)).one_or_none()


def get_comment(*, comment_id: int) -> AnswerCommentRead | None:
    """Select question."""

    comment = _get_comment(comment_id)

    return AnswerCommentRead.from_orm(comment) if comment is not None else None


def get_answer_comment_reaction(
    *, comment_id: int, user_id: int, code: str
) -> AnswerCommentReaction | None:
    """Select answer comment reaction."""

    return db.session.scalars(
        select(AnswerCommentReaction).filter_by(
            comment_id=comment_id, user_id=user_id, code=code
        )
    ).one_or_none()


def create_answer_comment_reaction(
    *, reaction_in: AnswerCommentReactionCreate
) -> AnswerCommentRead:
    """Insert answer comment reaction in table and return relevant comment."""

    comment = _get_comment(id=reaction_in.comment_id)

    reaction = AnswerCommentReaction(**reaction_in.dict())
    db.session.add(reaction)
    db.session.commit()

    return AnswerCommentRead.from_orm(comment)


def delete_answer_comment_reaction(
    *, comment_id: int, user_id: int, code: str
) -> AnswerCommentRead:
    """Delete answer comment reaction and return relevant answer comment."""

    reaction = get_answer_comment_reaction(
        comment_id=comment_id, user_id=user_id, code=code
    )
    db.session.delete(reaction)
    db.session.commit()

    comment = get_comment(comment_id=comment_id)
    return AnswerCommentRead.from_orm(comment)


def update_answer_comment_adding_history(
    *, comment_in: AnswerCommentUpdate
) -> AnswerCommentRead:
    """Update comment, insert comment history in table."""

    comment = _get_comment(comment_in.id)

    history_in = AnswerCommentHistoryCreate(
        comment_id=comment.id, content=comment.content
    )
    history = AnswerCommentHistory(**history_in.dict())
    db.session.add(history)

    updated_data = comment_in.dict(include={"content", "updated_at"})
    for column, value in updated_data.items():
        setattr(comment, column, value)

    db.session.commit()

    return AnswerCommentRead.from_orm(comment)
