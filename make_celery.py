"""
This is the module for running Celery app.
"""

from flow2and4.app import create_app
import os

mode = os.getenv("CELERY_MODE") or "dev"
flask_app = create_app(mode)
celery_app = flask_app.extensions["celery"]
