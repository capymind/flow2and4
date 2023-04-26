"""
This is module for handling http requests.
"""

from flask import Blueprint, render_template


bp = Blueprint("csduck", __name__, template_folder="templates", url_prefix="/")


@bp.get("/")
def index():
    """Show home page."""

    return render_template("index.html.jinja")
