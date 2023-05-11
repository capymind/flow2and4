"""
This is the module for handling all http requests related to pg.
"""


from http import HTTPMethod
from flask import Blueprint, render_template

bp = Blueprint(
    "cn",
    __name__,
    static_folder="static",
    template_folder="templates",
    url_prefix="/networking",
)


@bp.route("/", methods=[HTTPMethod.GET])
def index():
    """Show CN(Computer Networking) index page."""

    return render_template("cn/index.html.jinja")

