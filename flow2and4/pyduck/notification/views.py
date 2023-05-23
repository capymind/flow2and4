"""
This is the module for handling all requests related to pyduck notificaton.
"""

from http import HTTPMethod

from flask import Blueprint, render_template
from flask_login import login_required

bp = Blueprint(
    "notification",
    __name__,
    static_folder="static",
    template_folder="templates",
    url_prefix="/notifications",
)


@bp.route("/bell")
@login_required
def bell():
    """Return bell fragment."""
    a = 1
    return render_template("notification/bell.html.jinja")


@bp.route("/", methods=[HTTPMethod.GET])
def index():
    """Show notification index page."""

    return render_template("notification/index.html.jinja")
