"""
This is the module for handling requests related to pyduck auth.
"""

from flask import Blueprint, render_template, request
from http import HTTPStatus, HTTPMethod

bp = Blueprint("auth", __name__, template_folder="templates", url_prefix="/auth")


@bp.route("/sign-up", methods=[HTTPMethod.GET, HTTPMethod.POST])
def sign_up():
    """
    (GET) Show sign up page.
    (POST) Process sign up.
    """

    if request.method == HTTPMethod.POST:
        print(request.form.to_dict())

    return {"message": "success"}
