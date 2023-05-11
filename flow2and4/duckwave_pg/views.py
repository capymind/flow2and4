"""
This is the module for handling all http requests related to pg.
"""


from http import HTTPMethod
from flask import Blueprint, render_template

bp = Blueprint(
    "pg",
    __name__,
    static_folder="static",
    template_folder="templates",
    url_prefix="/programming",
)


@bp.route("/", methods=[HTTPMethod.GET])
def index():
    """Show PG(Programming) index page."""

    return render_template("pg/index.html.jinja")


@bp.route("/<topic>", methods=[HTTPMethod.GET])
def topic(topic: str):
    """Show Inheritance and Object-oriented Design page."""

    return render_template(f"pg/{topic}.html.jinja")