"""
This is the module for defining database transactions related to pyduck notification.

[services]
create_notification
delete_notification
get_all_notifications_by_commons

get_all_unread_notifications
make_unread_notification_read
"""

from flask_login import current_user
from flask_sqlalchemy.pagination import Pagination
from sqlalchemy import select

from flow2and4.database import db
from flow2and4.pyduck.notification.models import (
    Notification,
    NotificationForAnswerCommentReaction,
    NotificationForAnswerReaction,
    NotificationForPostComment,
    NotificationForPostCommentReaction,
    NotificationForPostReaction,
    NotificationForPostVote,
    NotificationForQuestionReaction
)
from flow2and4.pyduck.notification.schemas import (
    NotificationForAnswerCommentReactionCreate,
    NotificationForAnswerReactionCreate,
    NotificationForPostCommentCreate,
    NotificationForPostCommentReactionCreate,
    NotificationForPostReactionCreate,
    NotificationForPostVoteCreate,
    NotificationForQuestionReactionCreate
)


def create_notification(*, notification_in):
    """Insert notification data in table."""

    notification = None
    if isinstance(notification_in, NotificationForPostVoteCreate):
        notification = NotificationForPostVote(**notification_in.dict())

    elif isinstance(notification_in, NotificationForPostCommentCreate):
        notification = NotificationForPostComment(**notification_in.dict())

    elif isinstance(notification_in, NotificationForPostReactionCreate):
        notification = NotificationForPostReaction(**notification_in.dict())

    elif isinstance(notification_in, NotificationForPostCommentReactionCreate):
        notification = NotificationForPostReaction(**notification_in.dict())

    elif isinstance(notification_in, NotificationForQuestionReactionCreate):
        notification = NotificationForPostReaction(**notification_in.dict())

    elif isinstance(notification_in, NotificationForAnswerReactionCreate):
        notification = NotificationForPostReaction(**notification_in.dict())

    elif isinstance(notification_in, NotificationForAnswerCommentReactionCreate):
        notification = NotificationForPostReaction(**notification_in.dict())

    if notification is not None:
        db.session.add(notification)
        db.session.commit()


def delete_notification(
    *,
    user_id: int,
    notification_type: str,
    notification_target_id: int,
    from_user_id: int,
    to_user_id: int,
    notification_value: str | None = None
):
    """Delete notification data in table."""
    model = None
    notification = None

    if notification_type == "vote_post":
        model = NotificationForPostVote
    elif notification_type == "create_post_comment":
        model = NotificationForPostComment
    elif notification_type == "reaction_post":
        model = NotificationForPostReaction
    elif notification_type == "reaction_post_comment":
        model = NotificationForPostCommentReaction
    elif notification_type == "reaction_question":
        model = NotificationForQuestionReaction
    elif notification_type == "reaction_answer":
        model = NotificationForAnswerReaction
    elif notification_type == "reaction_answer_comment":
        model = NotificationForAnswerCommentReaction

    if model is not None:
        notification = db.session.scalars(
            select(model).filter_by(
                user_id=user_id,
                notification_type=notification_type,
                notification_target_id=notification_target_id,
                notification_value=notification_value,
                from_user_id=from_user_id,
                to_user_id=to_user_id,
            )
        ).one()

    if notification is not None:
        db.session.delete(notification)
        db.session.commit()


def get_all_notifications_by_commons(
    *, page, per_page, max_per_page, filters, sorters, periods, query
) -> Pagination:
    """Select all notifications by common parameters.

    TODO
    : non maintable, not flexible...
    : Microsoft API Guideline
    """

    select_ = select(Notification).filter_by(user_id=current_user.id)
    select_ = select_.order_by(*[Notification.created_at.desc()])

    return db.paginate(select_, page=page, per_page=per_page, max_per_page=max_per_page)


def mark_all_unread_notifications_as_read():
    """Get all unread notifications and mark them as read."""

    notifications = db.session.scalars(
        select(Notification).filter_by(user_id=current_user.id, read=False)
    ).all()

    for notification in notifications:
        notification.read = True

    db.session.commit()
