"""
This is the module for handling requets related to faduck root.
"""

from flask import Blueprint, render_template


bp = Blueprint("faduck", __name__, template_folder="templates", url_prefix="/")


@bp.route("/")
def index():
    """Show faduck index page."""

    return render_template("faduck/index.html.jinja")
