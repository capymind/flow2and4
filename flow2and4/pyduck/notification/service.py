"""
This is the module for defining database transactions related to pyduck notification.
"""

from sqlalchemy import select

from flow2and4.database import db
from flow2and4.pyduck.notification.models import (
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
