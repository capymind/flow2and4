"""
This is the module for defining email operations and related configurations.
"""

import smtplib
from email.message import EmailMessage

from flask import current_app


def send_message_using_gmail(message: EmailMessage):
    """Send message using gmail."""

    host = current_app.config.get("GMAIL_SMTP_HOST")
    port = current_app.config.get("GMAIL_SMTP_PORT")
    user = current_app.config.get("GMAIL_SMTP_LOGIN_USERNAME")
    password = current_app.config.get("GMAIL_SMTP_LOGIN_PASSWORD")

    with smtplib.SMTP(host=host, port=port) as s:
        s.starttls()
        s.login(
            user=user,
            password=password,
        )

        s.send_message(message)
