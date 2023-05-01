"""
This is the module for handling all http requests related to os.
"""


from http import HTTPMethod
from flask import Blueprint, render_template

bp = Blueprint(
    "os",
    __name__,
    static_folder="static",
    template_folder="templates",
    url_prefix="/operating-systems",
)


@bp.route("/", methods=[HTTPMethod.GET])
def index():
    """Show OS(Operating Systems) index page."""

    return render_template("os/index.html.jinja")


@bp.route("/<topic>", methods=[HTTPMethod.GET])
def topic(topic: str):
    """Show specific topic page."""

    return render_template(f"os/{topic}.html.jinja")