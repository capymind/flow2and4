"""
This is the module for defining configuration to flask application.
"""

from pydantic import BaseSettings


class WebConfig(BaseSettings):
    """Represent default configuration."""

    # A secret key that will be used for securely signing the session cookie
    # and can be used for any other security related needs by extensions or
    # csduck application. It should be a long random `bytes` or `str`.
    SECRET_KEY: str

    # The database connection URI used for the default engine.
    SQLALCHEMY_DATABASE_URI: str
    SQLALCHEMY_BINDS: dict

    # The page they were attempting to access will be passed in the `next`
    # query string variable, so you can redirect there if present instead of
    # the homepage. Alternatively(NOW), it will be added to the session as
    # `next` if `USE_SESSION_FOR_NEXT` is set.
    USE_SESSION_FOR_NEXT: bool = True

    # Google G-mail SMTP configuration.
    GMAIL_SMTP_HOST: str = "smtp.gmail.com"
    GMAIL_SMTP_PORT: int = 587
    GMAIL_SMTP_LOGIN_USERNAME: str
    GMAIL_SMTP_LOGIN_PASSWORD: str

    # Redis for Server-Sent Events.
    REDIS_CONNECTION_URL_FOR_SERVER_SENT_EVENTS: str

    # Celery.
    CELERY: dict

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"


class WebTestConfig(WebConfig):
    """Represent _TEST_ environment configuration."""

    class Config:
        env_file = [".env", ".env.test"]


class WebProdConfig(WebConfig):
    """Represent _PRODUCTION(prod)_ environment configuration."""

    class Config:
        env_file = [".env", ".env.prod"]
