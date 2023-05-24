"""
This is the module for handling all requests related to pyduck notificaton.
"""

from http import HTTPMethod

from flask import Blueprint, render_template, make_response
from flask_login import login_required
from flow2and4.pyduck.schemas import CommonParameters
from flow2and4.pyduck.notification.service import (
    get_all_notifications_by_commons,
    mark_all_unread_notifications_as_read,
)

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

    commons = CommonParameters()

    pagination = get_all_notifications_by_commons(**commons.dict())

    return render_template("notification/bell.html.jinja", pagination=pagination)


@bp.route("/bell/read")
@login_required
def bell_read():
    """Make notifications read because user click the bell and return fragment."""

    mark_all_unread_notifications_as_read()

    res = make_response()
    res.headers["HX-Trigger"] = "notificationread"

    return res


@bp.route("/", methods=[HTTPMethod.GET])
def index():
    """Show notification index page."""

    return render_template("notification/index.html.jinja")
