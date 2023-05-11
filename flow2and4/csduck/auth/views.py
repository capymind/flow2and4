"""
This is the module for handling http requests related to auth.
"""

from flask import (
    Blueprint,
    render_template,
    request,
    abort,
    make_response,
    url_for,
    redirect,
)
from http import HTTPStatus, HTTPMethod
from flow2and4.auth.schemas import (
    UserCreate,
    UserEmailVerificationCreate,
    UserAvatarCreate,
)
from flow2and4.auth.service import (
    is_duplicate,
    create_user,
    create_user_email_verification,
    get_user_by_username,
    get_user_for_session,
    create_user_avatar,
)
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
import json
from uuid import uuid4

bp = Blueprint(
    "auth",
    __name__,
    static_folder="static",
    template_folder="templates",
    url_prefix="/auth",
)


@bp.route("/sign-up", methods=[HTTPMethod.GET, HTTPMethod.POST])
def sign_up():
    """
    (GET) show sign up page.
    (POST) process sign up request.
    """

    if request.method == HTTPMethod.POST:
        errors = []
        user_in = None

        try:
            user_in = UserCreate(**request.form.to_dict())
        except:
            abort(HTTPStatus.BAD_REQUEST)

        if is_duplicate(field="username", value=user_in.username):
            errors.append("usernameexists")
        if is_duplicate(field="nickname", value=user_in.nickname):
            errors.append("nicknameexists")

        if errors:
            res = make_response({"message": errors})
            res.headers["HX-Trigger-After-Settle"] = json.dumps(
                {key: "" for key in errors}
            )

            return res

        user_in.password = generate_password_hash(user_in.password)
        user = create_user(user_in=user_in)

        user_email_verification_in = UserEmailVerificationCreate(
            user_id=user.id,
            vcode=uuid4().hex,
        )
        user_email_verification = create_user_email_verification(
            user_email_verification_in=user_email_verification_in
        )

        user_avatar_in = UserAvatarCreate(user_id=user.id)
        create_user_avatar(user_avatar_in=user_avatar_in)

        # TODO: send actual email.
        res = make_response(
            render_template("auth/email_verification.html.jinja", user=user)
        )
        res.headers["HX-Reswap"] = "outerHTML"
        return res

    return render_template("auth/sign_up.html.jinja")


@bp.route("/sign-in", methods=[HTTPMethod.GET, HTTPMethod.POST])
def sign_in():
    """
    (GET) show sign in page.
    (POST) process sign in request.
    """

    if request.method == HTTPMethod.POST:
        errors = []

        username = request.form.get("username")
        password = request.form.get("password")

        if username is None or password is None:
            abort(HTTPStatus.BAD_REQUEST)

        user = get_user_by_username(username=username)

        if user is None:
            errors.append("wronguser")
        elif not check_password_hash(user.password, password):
            errors.append("wrongpassword")

        if errors:
            res = make_response({"message": "errors"})
            res.headers["HX-Trigger-After-Settle"] = json.dumps(
                {key: "" for key in errors}
            )
            return res

        user = get_user_for_session(id=user.id)
        login_user(user)

        res = make_response({"message": "signinsuccess"})
        res.headers["HX-Redirect"] = url_for("csduck.index")
        return res

    return render_template("auth/sign_in.html.jinja")


@bp.get("/sign-out")
@login_required
def sign_out():
    """Sign user out."""
    logout_user()

    return redirect(url_for("csduck.index"))


@bp.route("/forgot-password", methods=[HTTPMethod.GET])
def forgot_password():
    """
    (GET) show forgot password page.
    """

    return render_template("auth/forgot_password.html.jinja")
