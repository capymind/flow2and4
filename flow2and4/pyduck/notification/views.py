"""
This is the module for handling all requests related to pyduck notificaton.
"""

from http import HTTPMethod

from flask import Blueprint, render_template

bp = Blueprint(
    "notification",
    __name__,
    static_folder="static",
    template_folder="templates",
    url_prefix="/notifications",
)


@bp.route("/", methods=[HTTPMethod.GET])
def index():
    """Show notification index page."""

    return render_template("notification/index.html.jinja")
