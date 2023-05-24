"""
This is the module for running Celery app.
"""

from flow2and4.app import create_app

flask_app = create_app()
celery_app = flask_app.extensions["celery"]
