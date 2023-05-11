"""
This is the module for defining fixtures used across tests.
"""

import pytest

from flask import Flask
from flow2and4.database import db as db_
from flow2and4.app import create_app


@pytest.fixture(scope="session")
def app():
    """Represent csduck application."""

    app = create_app(mode="test")

    yield app


@pytest.fixture(scope="session")
def db(app):
    with app.app_context():
        db_.create_all()
        yield db_
        db_.drop_all()


@pytest.fixture(scope="function")
def db_session(app):
    with app.app_context():
        
        db_.drop_all()
        db_.create_all()
        yield db_
        db_.drop_all()
