"""
This is the module for handling all http requests related to ms.
"""


from http import HTTPMethod
from flask import Blueprint, render_template

bp = Blueprint(
    "ms",
    __name__,
    static_folder="static",
    template_folder="templates",
    url_prefix="/machine-structures",
)


@bp.route("/", methods=[HTTPMethod.GET])
def index():
    """Show MS(Machine Structures) index page."""

    return render_template("ms/index.html.jinja")