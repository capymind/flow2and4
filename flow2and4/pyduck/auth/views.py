"""
This is the module for handling requests related to pyduck auth.
"""

import uuid
import json
from pydantic import ValidationError
from flask import (
    Blueprint,
    render_template,
    request,
    abort,
    make_response,
    redirect,
    url_for,
)
from flask_bcrypt import generate_password_hash, check_password_hash
from http import HTTPStatus, HTTPMethod
from flask_login import login_user, logout_user, login_required, current_user
from flow2and4.pyduck.auth.schemas import (
    UserCreate,
    UserAvatarCreate,
    UserBackdropCreate,
    UserVerificationEmailCreate,
)
from flow2and4.pyduck.auth.service import (
    does_field_value_exist,
    create_user,
    get_user_by_username,
    create_user_avatar,
    create_user_verification_email,
    get_user_verification_email,
    verify_user,
    create_user_backdrop,
    update_about_me,
)
from flow2and4.pyduck.auth.helpers import send_sign_up_verification_email

bp = Blueprint(
    "auth",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/auth",
)


@bp.route("/sign-up", methods=[HTTPMethod.GET, HTTPMethod.POST])
def sign_up():
    """
    (GET) Show sign up page.
    (POST) Process sign up.
    """

    if request.method == HTTPMethod.POST:
        try:
            user_in = UserCreate(**request.form.to_dict())
            user_in.password = generate_password_hash(user_in.password)

        except ValidationError:
            abort(HTTPStatus.BAD_REQUEST)

        errors = []
        if does_field_value_exist("username", user_in.username):
            errors.append("username-exists")
        if does_field_value_exist("nickname", user_in.nickname):
            errors.append("nickname-exists")

        if len(errors) > 0:
            res = make_response()
            res.headers["HX-Trigger"] = json.dumps({key: "" for key in errors})
            return res, HTTPStatus.BAD_REQUEST

        user = create_user(user_in=user_in)

        avatar_in = UserAvatarCreate(user_id=user.id)
        create_user_avatar(avatar_in=avatar_in)

        backdrop_in = UserBackdropCreate(user_id=user.id)
        create_user_backdrop(backdrop_in=backdrop_in)

        verification_in = UserVerificationEmailCreate(
            user_id=user.id, vcode=uuid.uuid4().hex
        )
        verification = create_user_verification_email(verification_in=verification_in)

        send_sign_up_verification_email(user=user, verification=verification)

        res = make_response()
        res.headers["HX-Trigger-After-Settle"] = "user-created"

        return res, HTTPStatus.CREATED

    return {"message": "success"}


@bp.route("/sign-up/verification", methods=[HTTPMethod.GET])
def sign_up_verification():
    """
    (GET) Process sign up verification.
    """

    username = request.args.get("username")
    vcode = request.args.get("vcode")

    if username is None or vcode is None:
        abort(HTTPStatus.BAD_REQUEST)

    user = get_user_by_username(username=username)
    if user is None:
        abort(HTTPStatus.BAD_REQUEST)

    verification = get_user_verification_email(user_id=user.id)

    if verification is None:
        abort(HTTPStatus.BAD_REQUEST)
    if vcode != verification.vcode:
        abort(HTTPStatus.BAD_REQUEST)

    verified_user = verify_user(user_id=user.id)

    return redirect(url_for("pyduck.auth.welcome"))


@bp.route("/sign-up/welcome", methods=[HTTPMethod.GET])
def welcome():
    """
    (GET) Show welcome page after signing up successfully.
    """

    return render_template("auth/welcome.html.jinja")


@bp.route("/sign-in", methods=[HTTPMethod.GET, HTTPMethod.POST])
def sign_in():
    """
    (GET) Show sign in page.
    (POST) Process sign in.
    """

    username = request.form.get("username")
    password = request.form.get("password")

    user = get_user_by_username(username=username)

    res = make_response()
    if user is None:
        res.headers["HX-Trigger"] = "username-dont-exist"
        return res, HTTPStatus.UNAUTHORIZED

    if not check_password_hash(user.password, password):
        res.headers["HX-Trigger"] = "password-dont-match"
        return res, HTTPStatus.UNAUTHORIZED

    login_user(user)
    res.headers["HX-Redirect"] = url_for("pyduck.index")

    return res


@bp.route("/sign-out", methods=[HTTPMethod.GET])
def sign_out():
    """Sign user out."""

    logout_user()

    return redirect(url_for("pyduck.index"))


@bp.route("/settings/profile", methods=[HTTPMethod.GET])
@login_required
def profile_setting():
    """
    (GET) Show my profile setting page.
    """

    return render_template("auth/profile_setting.html.jinja")


@bp.route("/me/about_me", methods=[HTTPMethod.POST])
@login_required
def about_me():
    """
    (POST) Save about me and return relevant event.
    """

    content = request.form.get("about_me")
    
    # validation needed
    update_about_me(user_id=current_user.id, about_me=content)

    