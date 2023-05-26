"""
This is the module for defining helpers related to pyduck auth.

[helper]
send_sign_up_verification_email
send_forgot_password_gamil
validate_plain_password
"""

import re
import logging
from email.headerregistry import Address
from email.message import EmailMessage

from flask import get_template_attribute, url_for

from flow2and4.pyduck.auth.schemas import (
    UserForgotPasswordEmailVerificationRead,
    UserRead,
    UserVerificationEmailRead,
)
from flow2and4.pyduck.utils.email import send_message_using_gmail

logger = logging.getLogger(__name__)


def send_sign_up_verification_email(
    user: UserRead, verification: UserVerificationEmailRead
):
    """Send sigup verification email."""

    message = EmailMessage()
    message["Subject"] = "pyduck 회원가입 인증메일"

    username, domain = user.username.split("@")
    message["To"] = Address(username=username, domain=domain)
    message["From"] = Address(
        display_name="pyduck 로디", username="mfs.rodi", domain="gmail.com"
    )

    template = get_template_attribute(
        "auth/emails/signup_verification.html.jinja", "verification"
    )
    verification_url = url_for(
        "pyduck.auth.sign_up_verification",
        username=user.username,
        vcode=verification.vcode,
        _external=True,
    )
    message.add_alternative(template(verification_url=verification_url), subtype="html")

    send_message_using_gmail(message)
    logger.info("send sign up verification email successfully.")


def send_forgot_password_email(
    user: UserRead, verification: UserForgotPasswordEmailVerificationRead
):
    """Send forgot password email for redirecting user to set password."""

    message = EmailMessage()
    message["Subject"] = "pyduck 비밀번호 초기화메일"

    username, domain = user.username.split("@")
    message["To"] = Address(username=username, domain=domain)
    message["From"] = Address(
        display_name="pyduck 로디", username="mfs.rodi", domain="gmail.com"
    )

    template = get_template_attribute(
        "auth/emails/forgot_password.html.jinja", "template"
    )

    message.add_alternative(
        template(user=user, verification=verification), subtype="html"
    )
    send_message_using_gmail(message)
    logger.info("send forgot password email successfully.")


def validate_plain_password(password: str) -> bool:
    """validate whether plain password follows pyduck's password constraints.

    constraints
        - (constraint1) 8-30 letters
        - (constraint2) at least one uppercase
        - (constraint3) at least one lowercase
        - (constraint4) at least one number
        - (constraint5) at least one special characters(`~!@#$%^&*()_+-=)
    """

    # constraint1
    if len(password) < 8 or len(password) > 30:
        return False

    # constraint2
    at_least_one_uppercase = False
    for char_ in password:
        if char_.isupper():
            at_least_one_uppercase = True
    if not at_least_one_uppercase:
        return False

    # constraint3
    at_least_one_lowercase = False
    for char_ in password:
        if char_.islower():
            at_least_one_lowercase = True
    if not at_least_one_lowercase:
        return False

    # constraint4
    at_least_one_number = False
    for char_ in password:
        if char_.isdigit():
            at_least_one_number = True
    if not at_least_one_number:
        return False

    # constraint5
    at_least_one_special = False
    for char_ in "`~!@#$%^&*()_+-=":
        if char_ in password:
            at_least_one_special = True
    if not at_least_one_special:
        return False

    return True


def validate_nickname(nickname: str) -> bool:
    """validate whether nickname follows pyduck's nickname constraints.

    constraints
        - (constraints1) 2-20 letters
        - (constraints2) no any kind of white space
        - (constraints3) korean, english, digit, dash, underscore only.
    """
    
    # constraint1
    if len(nickname) < 2 or len(nickname) > 20:
        return False

    # constraint2
    if len(nickname) != len(nickname.replace(" ", "")):
        return False

    # constraint3
    if re.match(r"^[가-힣a-zA-Z0-9-_]{2,20}$", nickname) is None:
        return False

    return True
