"""
This is the module for handling routes related to rodi.
"""

from flask import Blueprint, render_template



bp = Blueprint("rodi", __name__, template_folder="templates", url_prefix="/")


@bp.route("/")
def index():
    """Show main index page."""
    return render_template("rodi/index.html.jinja")
