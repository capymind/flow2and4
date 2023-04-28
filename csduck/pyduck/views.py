"""
This is the module for handling requests related to pyduck.
"""

from flask import Blueprint, render_template
from csduck.pyduck.auth.views import bp as bp_auth

bp = Blueprint("pyduck", __name__, template_folder="templates", url_prefix="/")
bp.register_blueprint(bp_auth)

@bp.route("/")
def index():
    """Show pyduck main index page."""

    return render_template("pyduck/index.html.jinja")
