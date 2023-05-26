"""
This is the module for handling database transactions related to pyduck auth.

[service]
does_field_value_exist
create_user
_get_user
get_user
delete_user
get_pyduck_user_for_session
get_user_by_username
get_user_by_nickname
create_user_avatar
create_user_backdrop
create_user_verification_email
get_user_verification_email
create_user_forgot_password_email_verification
delete_user_forgot_password_email_verification
verify_user
update_about_me
delete_and_create_user_sns
_get_user_sns_by_user_id
get_user_sns_by_user_id
_get_user_avatar_by_user_id
get_user_avatar_by_user_id
_get_user_backdrop_by_user_id
get_user_backdrop_by_user_id
_get_user_backdrop
update_user_backdrop
_get_user_avatar
update_user_avatar
create_user_action
delete_user_action
get_all_user_actions_by_commons_and_action_types
update_password
update_nickname
"""

from flask_sqlalchemy.pagination import Pagination
from sqlalchemy import select

from flow2and4.database import db
from flow2and4.pyduck.auth.models import (
    User,
    UserAction,
    UserActionCreateAnswer,
    UserActionCreateAnswerComment,
    UserActionCreatePost,
    UserActionCreatePostComment,
    UserActionCreateQuestion,
    UserActionReactionAnswer,
    UserActionReactionAnswerComment,
    UserActionReactionPost,
    UserActionReactionPostComment,
    UserActionReactionQuestion,
    UserActionVote,
    UserActionVoteAnswer,
    UserActionVotePost,
    UserActionVotePostComment,
    UserActionVoteQuestion,
    UserAvatar,
    UserBackdrop,
    UserForgotPasswordEmailVerification,
    UserSns,
    UserVerificationEmail,
)
from flow2and4.pyduck.auth.schemas import (
    UserActionCreateAnswerCommentCreate,
    UserActionCreateAnswerCreate,
    UserActionCreatePostCommentCreate,
    UserActionCreatePostCreate,
    UserActionCreatePostRead,
    UserActionCreateQuestionCreate,
    UserActionReactionAnswerCommentCreate,
    UserActionReactionAnswerCreate,
    UserActionReactionPostCommentCreate,
    UserActionReactionPostCreate,
    UserActionReactionQuestionCreate,
    UserActionVoteAnswerCreate,
    UserActionVotePostCommentCreate,
    UserActionVotePostCreate,
    UserActionVotePostRead,
    UserActionVoteQuestionCreate,
    UserAvatarCreate,
    UserAvatarRead,
    UserAvatarUpdate,
    UserBackdropCreate,
    UserBackdropRead,
    UserBackdropUpdate,
    UserCreate,
    UserForgotPasswordEmailVerificationCreate,
    UserForgotPasswordEmailVerificationRead,
    UserRead,
    UserReadForSession,
    UserSnsCreate,
    UserSnsRead,
    UserVerificationEmailCreate,
    UserVerificationEmailRead,
)
from flow2and4.pyduck.community.models import (
    AnswerVote,
    PostCommentVote,
    PostVote,
    QuestionVote,
    Vote,
)


def does_field_value_exist(field: str, value: str | int | float) -> bool:
    """Check table column's value."""

    condition = getattr(User, field) == value
    return bool(db.session.scalars(select(User).where(condition)).one_or_none())


def create_user(*, user_in: UserCreate) -> UserRead:
    """Insert user in table."""

    user = User(**user_in.dict())
    db.session.add(user)
    db.session.commit()

    return UserRead.from_orm(user)


def _get_user(id: int) -> User | None:
    """Select user by id."""
    return db.session.scalars(select(User).filter_by(id=id)).one_or_none()


def get_user(*, id: int) -> UserRead | None:
    user = _get_user(id=id)
    return UserRead.from_orm(user) if user else None


def delete_user(*, id: int) -> None:
    """Delete user in table."""

    user = _get_user(id)
    db.session.delete(user)
    db.session.commit()


def get_pyduck_user_for_session(*, id: int) -> UserReadForSession:
    """Select user for sign-in session."""
    user = _get_user(id=id)
    return UserReadForSession.from_orm(user)


def get_user_by_username(*, username: str) -> UserReadForSession | None:
    """Select user by username for sign-in session."""

    user = db.session.scalars(select(User).filter_by(username=username)).one_or_none()

    return UserReadForSession.from_orm(user) if user is not None else None


def get_user_by_nickname(*, nickname: str) -> UserRead | None:
    """Select user by username for sign-in session."""

    user = db.session.scalars(select(User).filter_by(nickname=nickname)).one_or_none()

    return UserRead.from_orm(user) if user is not None else None


def create_user_avatar(*, avatar_in: UserAvatarCreate) -> UserAvatarRead:
    """Insert user avatar in table."""

    avatar = UserAvatar(**avatar_in.dict())
    db.session.add(avatar)
    db.session.commit()

    return UserAvatarRead.from_orm(avatar)


def create_user_backdrop(*, backdrop_in: UserBackdropCreate) -> UserBackdropRead:
    """Insert user backdrop in table."""

    backdrop = UserBackdrop(**backdrop_in.dict())
    db.session.add(backdrop)
    db.session.commit()

    return UserBackdropRead.from_orm(backdrop)


def create_user_verification_email(
    *, verification_in: UserVerificationEmailCreate
) -> UserVerificationEmailRead:
    """Insert user verification email in table."""

    verification = UserVerificationEmail(**verification_in.dict())

    db.session.add(verification)
    db.session.commit()

    return UserVerificationEmailRead.from_orm(verification)


def create_user_forgot_password_email_verification(
    *, verification_in: UserForgotPasswordEmailVerificationCreate
) -> None:
    """Insert user forgot password email verification in table."""

    verification = UserForgotPasswordEmailVerification(**verification_in.dict())

    db.session.add(verification)
    db.session.commit()


def delete_user_forgot_password_email_verification(*, user_id: int) -> None:
    """Delete user forgot password email verification in table."""

    verification = _get_user_forgot_password_email_verification(user_id)
    if verification is not None:
        db.session.delete(verification)
        db.session.commit()


def get_user_verification_email(*, user_id: int) -> UserVerificationEmailRead | None:
    """Select user verification email."""

    verification = db.session.scalars(
        select(UserVerificationEmail).filter_by(user_id=user_id)
    ).one_or_none()

    return (
        UserVerificationEmailRead.from_orm(verification)
        if verification is not None
        else None
    )


def _get_user_forgot_password_email_verification(user_id):
    return db.session.scalars(
        select(UserForgotPasswordEmailVerification).filter_by(user_id=user_id)
    ).one_or_none()


def get_user_forgot_password_email_verification(
    *, user_id: int
) -> UserForgotPasswordEmailVerificationRead | None:
    """Select user's forgot password email verification."""

    verification = _get_user_forgot_password_email_verification(user_id)

    return (
        UserForgotPasswordEmailVerificationRead.from_orm(verification)
        if verification is not None
        else None
    )


def verify_user(*, user_id: int) -> UserRead:
    """Change user's verified to true(verified)."""

    user = _get_user(id=user_id)
    user.verified = True
    db.session.commit()

    return UserRead.from_orm(user)


def update_about_me(*, user_id: int, about_me: str) -> None:
    """Update user's about_me."""

    user = _get_user(user_id)
    setattr(user, "about_me", about_me)
    db.session.commit()


def delete_and_create_user_sns(
    *, user_id: int, snss_in: list[UserSnsCreate]
) -> list[UserSnsRead]:
    """Delete user's old sns and replace(create) it with new sns."""

    user = _get_user(user_id)
    user.sns = []

    snss = []
    for sns_in in snss_in:
        snss.append(UserSns(**sns_in.dict()))

    db.session.add_all(snss)
    db.session.commit()

    return [UserSnsRead.from_orm(sns) for sns in snss]


def _get_user_sns_by_user_id(*, user_id) -> list[UserSns | None]:
    """Get user sns by user id."""
    return db.session.scalars(select(UserSns).filter_by(user_id=user_id)).all()


def get_user_sns_by_user_id(*, user_id) -> list[UserSnsRead | None]:
    """Get user avatar by user id."""
    return [
        UserSnsRead.from_orm(sns) for sns in _get_user_sns_by_user_id(user_id=user_id)
    ]


def _get_user_avatar_by_user_id(*, user_id) -> UserAvatar:
    """Get user backdrop by user id."""
    return db.session.scalars(select(UserAvatar).filter_by(user_id=user_id)).one()


def get_user_avatar_by_user_id(*, user_id) -> UserAvatarRead:
    """Get user avatar by user id."""
    return _get_user_avatar_by_user_id(user_id=user_id)


def _get_user_backdrop_by_user_id(*, user_id) -> UserBackdrop:
    """Get user backdrop by user id."""
    return db.session.scalars(select(UserBackdrop).filter_by(user_id=user_id)).one()


def get_user_backdrop_by_user_id(*, user_id) -> UserBackdropRead:
    """Get user backdrop by user id."""
    return _get_user_backdrop_by_user_id(user_id=user_id)


def _get_user_backdrop(id) -> UserBackdrop:
    """Get user backdrop by id."""
    return db.session.scalars(select(UserBackdrop).filter_by(id=id)).one()


def update_user_backdrop(*, backdrop_in: UserBackdropUpdate) -> UserBackdropRead:
    """Update user's backdrop."""

    backdrop = _get_user_backdrop(backdrop_in.id)

    updated_data = backdrop_in.dict(
        exclude={
            "id",
        }
    )
    for column, value in updated_data.items():
        setattr(backdrop, column, value)

    db.session.commit()
    return UserBackdropRead.from_orm(backdrop)


def _get_user_avatar(id) -> UserAvatar:
    """Get user avatar by id."""
    return db.session.scalars(select(UserAvatar).filter_by(id=id)).one()


def update_user_avatar(*, avatar_in: UserAvatarUpdate) -> UserAvatarRead:
    """Update user's backdrop."""

    avatar = _get_user_avatar(avatar_in.id)

    updated_data = avatar_in.dict(
        exclude={
            "id",
        }
    )
    for column, value in updated_data.items():
        setattr(avatar, column, value)

    db.session.commit()
    return UserAvatarRead.from_orm(avatar)


def create_user_action(*, user_action_in):
    """Insert user action data in table."""

    user_action = None
    if isinstance(user_action_in, UserActionCreatePostCreate):
        user_action = UserActionCreatePost(**user_action_in.dict())

    elif isinstance(user_action_in, UserActionVotePostCreate):
        user_action = UserActionVotePost(**user_action_in.dict())

    elif isinstance(user_action_in, UserActionVotePostCommentCreate):
        user_action = UserActionVotePostComment(**user_action_in.dict())

    elif isinstance(user_action_in, UserActionVoteQuestionCreate):
        user_action = UserActionVoteQuestion(**user_action_in.dict())

    elif isinstance(user_action_in, UserActionVoteAnswerCreate):
        user_action = UserActionVoteAnswer(**user_action_in.dict())

    elif isinstance(user_action_in, UserActionCreateQuestionCreate):
        user_action = UserActionCreateQuestion(**user_action_in.dict())

    elif isinstance(user_action_in, UserActionCreatePostCommentCreate):
        user_action = UserActionCreatePostComment(**user_action_in.dict())

    elif isinstance(user_action_in, UserActionCreateAnswerCreate):
        user_action = UserActionCreateAnswer(**user_action_in.dict())

    elif isinstance(user_action_in, UserActionCreateAnswerCommentCreate):
        user_action = UserActionCreateAnswerComment(*user_action_in.dict())

    elif isinstance(user_action_in, UserActionReactionPostCreate):
        user_action = UserActionReactionPost(**user_action_in.dict())

    elif isinstance(user_action_in, UserActionReactionPostCommentCreate):
        user_action = UserActionReactionPostComment(**user_action_in.dict())

    elif isinstance(user_action_in, UserActionReactionQuestionCreate):
        user_action = UserActionReactionQuestion(**user_action_in.dict())

    elif isinstance(user_action_in, UserActionReactionAnswerCreate):
        user_action = UserActionReactionAnswer(**user_action_in.dict())

    elif isinstance(user_action_in, UserActionReactionAnswerCommentCreate):
        user_action = UserActionReactionAnswerComment(**user_action_in.dict())

    if user_action is None:
        raise Exception("invalid user action type")

    db.session.add(user_action)
    db.session.commit()

    return user_action


def delete_user_action(*, user_id, action_type, target_id, action_value: str = None):
    """Delete user action data in table."""

    model = None
    user_action = None

    if action_type == "vote_post":
        model = UserActionVotePost

    elif action_type == "vote_post_comment":
        model = UserActionVotePostComment

    elif action_type == "vote_question":
        model = UserActionVoteQuestion

    elif action_type == "vote_answer":
        model = UserActionVoteAnswer

    elif action_type == "create_post_comment":
        model = UserActionCreatePostComment

    elif action_type == "create_question":
        model = UserActionCreateQuestion

    elif action_type == "create_answer":
        model = UserActionCreateAnswer

    elif action_type == "create_answer_comment":
        model = UserActionCreateAnswerComment

    elif action_type == "reaction_post":
        model = UserActionReactionPost

    elif action_type == "reaction_post_comment":
        model = UserActionReactionPostComment

    elif action_type == "reaction_question":
        model = UserActionReactionQuestion

    elif action_type == "reaction_answer":
        model = UserActionReactionAnswer

    elif action_type == "reaction_answer_comment":
        model = UserActionReactionAnswerComment

    if model is not None:
        user_action = db.session.scalars(
            select(model).filter_by(
                user_id=user_id, target_id=target_id, action_value=action_value
            )
        ).one()

    if user_action is not None:
        db.session.delete(user_action)
        db.session.commit()


def get_all_user_actions_by_commons_and_action_types(
    *,
    page,
    per_page,
    max_per_page,
    filters,
    sorters,
    query,
    periods,
    action_types: list[str]
) -> Pagination:
    """Select all user actions given common parameters.

    TODO
    : not python... yet
    : repeat myself...
    """

    select_ = select(UserAction).where(UserAction.action_type.in_(action_types))

    # Filtering
    filters = [] if filters is None else filters.split()
    periods = [] if periods is None else periods.split()
    filters = filters + periods

    filter_conditions = []
    for filter_ in filters:
        field, op, value = filter_.split("-", 2)
        column = getattr(UserAction, field)

        # Operators
        if op == "eq":
            filter_conditions.append(column == value)

    select_ = select_.where(*filter_conditions)

    # Sorting.
    sorters = [] if sorters is None else sorters.split()
    sorter_conditions = [UserAction.created_at.desc()]  # default sorting.
    for sorter_ in sorters:
        field, direction = sorter_.split("-")
        column = getattr(UserAction, field)
        sorter_conditions.append(column.asc() if direction == "asc" else column.desc())
    select_ = select_.order_by(*sorter_conditions)

    return db.paginate(select_, page=page, per_page=per_page, max_per_page=max_per_page)


def update_password(user_id: int, password: str) -> None:
    """Update user's password."""

    user = _get_user(user_id)
    user.password = password
    db.session.commit()


def update_nickname(user_id: int, nickname: str) -> None:
    """Update user's nickname."""

    user = _get_user(user_id)
    user.nickname = nickname
    db.session.commit()
