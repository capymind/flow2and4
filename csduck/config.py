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

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class WebTestConfig(WebConfig):
    """Represent _TEST_ environment configuration."""

    class Config:
        env_file = [".env", ".env.test"]


class WebProdConfig(WebConfig):
    """Represent _PRODUCTION(prod)_ environment configuration."""

    class Config:
        env_file = [".env", ".env.prod"]
