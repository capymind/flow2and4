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
)
from csduck.pyduck.community.models import (
    QuestionImageUpload,
    Question,
    QuestionTag,
    QuestionHistory,
    QuestionVote,
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


def create_question_vote(vote_in: QuestionVoteCreate) -> QuestionVoteRead:
    """Insert question vote in table."""

    question = _get_question(id=vote_in.question_id)
    question.vote_count += 1

    vote = QuestionVote(**vote_in.dict())
    db.session.add(vote)
    db.session.commit()

    return QuestionVoteRead.from_orm(vote)
