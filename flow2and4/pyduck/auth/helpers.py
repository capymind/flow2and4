"""
This is the module for defining helpers related to pyduck auth.
"""

import logging
from email.headerregistry import Address
from email.message import EmailMessage

from flask import get_template_attribute, url_for

from flow2and4.pyduck.auth.schemas import UserRead, UserVerificationEmailRead
from flow2and4.pyduck.utils.email import send_message_using_gmail

logger = logging.getLogger(__name__)


def send_sign_up_verification_email(
    user: UserRead, verification: UserVerificationEmailRead
):
    """Send sigup verification email."""

    message = EmailMessage()
    message["Subject"] = f"💌pyduck 회원가입 인증메일"

    username, domain = user.username.split("@")
    message["To"] = Address(username=username, domain=domain)
    message["From"] = Address(display_name="👋pyduck 로디")

    template = get_template_attribute("auth/emails/signup_verification.html.jinja", "verification")
    verification_url = url_for(
        "pyduck.auth.sign_up_verification",
        username=user.username,
        vcode=verification.vcode,
        _external=True,
    )
    message.add_alternative(template(verification_url=verification_url), subtype="html")

    send_message_using_gmail(message)
    logger.info("send sign up verification email successfully")
