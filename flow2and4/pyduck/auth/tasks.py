"""
This is the module for defining background tasks related to pyduck auth.
"""

from celery import shared_task
from flow2and4.pyduck.auth.helpers import (
    send_sign_up_verification_email as _send_sign_up_verification_email,
)
from flow2and4.pyduck.auth.service import get_user, get_user_verification_email


@shared_task()
def send_sign_up_verification_email(user_id: int) -> None:
    """Send sign up verification email."""

    user = get_user(id=user_id)
    verification = get_user_verification_email(user_id=user_id)

    _send_sign_up_verification_email(user=user, verification=verification)
