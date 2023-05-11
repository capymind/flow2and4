"""
This is the module for handling routes related to myweb.
"""

from flask import Blueprint, render_template



bp = Blueprint("myweb", __name__, template_folder="templates", url_prefix="/")


@bp.route("/")
def index():
    """Show main index page."""
    return render_template("myweb/index.html.jinja")
