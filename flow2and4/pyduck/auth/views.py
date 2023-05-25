"""
This is the module for handling requests related to pyduck auth.

[ route handlers ]

/sign-up                                -> sign_up
/sign_up/verification                   -> sign_up_verification
/sign-up/welcome                        -> welcome
/sign-in                                -> sign_in
/sign-out                               -> sign_out
/profile/settings                       -> profile_setting
/me/about_me                            -> about_me
/me/sns                                 -> sns
/me/backdrop                            -> backdrop
/me/avatar                              -> avatar

/me/activity                            -> my_activity
/me/activity/questions-and-posts        -> my_activity_about_question_and_post
/me/activity/answers-and-comments       -> my_activity_about_answer_and_comment
/me/activity/votes                      -> my_activity_about_voting
/me/activity/reactions                  -> my_activity_about_reaction
"""

import time
import json
import os
import uuid
from http import HTTPMethod, HTTPStatus

from flask import (
    Blueprint,
    abort,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_bcrypt import check_password_hash, generate_password_hash
from flask_login import current_user, login_required, login_user, logout_user
from pydantic import ValidationError
from werkzeug.utils import secure_filename

from flow2and4.pyduck.auth.schemas import (
    UserAvatarCreate,
    UserAvatarUpdate,
    UserBackdropCreate,
    UserBackdropUpdate,
    UserCreate,
    UserSnsCreate,
    UserVerificationEmailCreate,
)
from flow2and4.pyduck.auth.service import (
    create_user,
    create_user_avatar,
    create_user_backdrop,
    create_user_verification_email,
    delete_and_create_user_sns,
    does_field_value_exist,
    get_all_user_actions_by_commons_and_action_types,
    get_user_avatar_by_user_id,
    get_user_backdrop_by_user_id,
    get_user_by_username,
    get_user_sns_by_user_id,
    get_user_verification_email,
    update_about_me,
    update_user_avatar,
    update_user_backdrop,
    verify_user,
)
from flow2and4.pyduck.community.service import (
    get_all_reactions_by_commons,
    get_all_votes_by_commons,
)
from flow2and4.pyduck.auth import tasks
from flow2and4.pyduck.schemas import CommonParameters

bp = Blueprint(
    "auth",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/auth",
)

bp_user = Blueprint(
    "user",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/users",
)

ALLOWED_SNS_PLATFORMS = ["github", "twitter", "other1", "other2"]


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

        snss_in = [
            UserSnsCreate(user_id=user.id, platform=sns)
            for sns in ALLOWED_SNS_PLATFORMS
        ]
        delete_and_create_user_sns(user_id=user.id, snss_in=snss_in)

        verification_in = UserVerificationEmailCreate(
            user_id=user.id, vcode=uuid.uuid4().hex
        )
        create_user_verification_email(verification_in=verification_in)

        tasks.send_sign_up_verification_email.delay(user.id)
        # tasks.add.delay(1, 2)
        time.sleep(3.0)  # minimum delay for sendign email.

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


@bp.route("/profile/settings", methods=[HTTPMethod.GET])
@login_required
def profile_setting():
    """
    (GET) Show my profile setting page.
    """

    backdrop = get_user_backdrop_by_user_id(user_id=current_user.id)
    avatar = get_user_avatar_by_user_id(user_id=current_user.id)
    snss = get_user_sns_by_user_id(user_id=current_user.id)

    return render_template(
        "auth/profile/settings/index.html.jinja",
        backdrop=backdrop,
        avatar=avatar,
        snss=snss,
    )


@bp.route("/me/about_me", methods=[HTTPMethod.POST])
@login_required
def about_me():
    """
    (POST) Save about me and return relevant event.
    """

    content = request.form.get("about_me")

    # validation needed
    update_about_me(user_id=current_user.id, about_me=content)

    res = make_response()
    res.headers["HX-Trigger-After-Settle"] = "about-me-modified-successfully"

    return res, HTTPStatus.OK


@bp.route("/me/sns", methods=[HTTPMethod.POST])
@login_required
def sns():
    """
    (POST) Save about sns return relevant event.
    """

    snss_in, snss = [], []
    for platform in ALLOWED_SNS_PLATFORMS:
        link = request.form.get(f"sns_{platform}")
        _p = request.form.get(f"sns_{platform}_public")
        public = True if _p == "true" else False

        if link is not None:
            snss_in.append(
                UserSnsCreate(
                    user_id=current_user.id, platform=platform, link=link, public=public
                )
            )

    if len(snss_in) > 0:
        snss = delete_and_create_user_sns(user_id=current_user.id, snss_in=snss_in)

    res = make_response(
        render_template("auth/profile/settings/sns.html.jinja", snss=snss)
    )
    res.headers["HX-Trigger-After-Settle"] = "sns-modified-successfully"

    return res, HTTPStatus.OK


@bp.route("/me/backdrop", methods=[HTTPMethod.PUT])
@login_required
def backdrop():
    """
    (PUT) Modify backdrop and return relevant fragment.
    """

    ALLOWED_BACKDROP_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
    old_backdrop = get_user_backdrop_by_user_id(user_id=current_user.id)
    old_filename = old_backdrop.filename

    file = request.files.get("backdrop")
    static_folder = bp.static_folder
    subpath = "images/backdrop"

    if file is None:
        abort(HTTPStatus.BAD_REQUEST)

    fileformat = None
    try:
        fileformat = file.filename.rsplit(".", 1)[-1]
    except:
        abort(HTTPStatus.BAD_REQUEST)

    if fileformat.lower() not in ALLOWED_BACKDROP_EXTENSIONS:
        abort(HTTPStatus.BAD_REQUEST)

    original_filename = secure_filename(file.filename)

    filename = f"{uuid.uuid4().hex}.{fileformat}"
    filepath = os.path.join(static_folder, subpath, filename)

    file.save(filepath)
    filesize = os.stat(filepath).st_size

    backdrop_in = UserBackdropUpdate(
        id=old_backdrop.id,
        user_id=current_user.id,
        url=url_for("pyduck.auth.static", filename=os.path.join(subpath, filename)),
        filename=filename,
        original_filename=original_filename,
        mimetype=file.mimetype,
        filesize=filesize,
    )

    backdrop = update_user_backdrop(backdrop_in=backdrop_in)

    if "default_backdrop" not in old_filename:
        os.remove(os.path.join(static_folder, subpath, old_filename))

    res = make_response(
        render_template("auth/profile/settings/backdrop.html.jinja", backdrop=backdrop)
    )
    res.headers["HX-Trigger-After-Settle"] = "backdrop-modified-successfully"

    return res, HTTPStatus.OK


@bp.route("/me/avatar", methods=[HTTPMethod.PUT])
@login_required
def avatar():
    """
    (PUT) Modify avatar and return relevant fragment.
    """

    ALLOWED_AVATAR_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
    old_avatar = get_user_avatar_by_user_id(user_id=current_user.id)
    old_filename = old_avatar.filename

    file = request.files.get("avatar")
    static_folder = bp.static_folder
    subpath = "images/avatar"

    if file is None:
        abort(HTTPStatus.BAD_REQUEST)

    fileformat = None
    try:
        fileformat = file.filename.rsplit(".", 1)[-1]
    except:
        abort(HTTPStatus.BAD_REQUEST)

    if fileformat.lower() not in ALLOWED_AVATAR_EXTENSIONS:
        abort(HTTPStatus.BAD_REQUEST)

    original_filename = secure_filename(file.filename)

    filename = f"{uuid.uuid4().hex}.{fileformat}"
    filepath = os.path.join(static_folder, subpath, filename)

    file.save(filepath)
    filesize = os.stat(filepath).st_size

    avatar_in = UserAvatarUpdate(
        id=old_avatar.id,
        user_id=current_user.id,
        url=url_for("pyduck.auth.static", filename=os.path.join(subpath, filename)),
        filename=filename,
        original_filename=original_filename,
        mimetype=file.mimetype,
        filesize=filesize,
    )

    avatar = update_user_avatar(avatar_in=avatar_in)

    if "default_avatar" not in old_filename:
        os.remove(os.path.join(static_folder, subpath, old_filename))

    res = make_response(
        render_template("auth/profile/settings/avatar.html.jinja", avatar=avatar)
    )
    res.headers["HX-Trigger-After-Settle"] = "avatar-modified-successfully"

    return res, HTTPStatus.OK


@bp_user.route("/me/activity", methods=[HTTPMethod.GET])
def my_activity():
    """
    (GET) Show my activity index page.
    """

    commons = CommonParameters(**request.args.to_dict())
    commons.filters = f"user_id-eq-{current_user.id}"

    action_types = [
        "create_post",
        "create_question",
        "create_answer",
        "create_answer_comment",
        "create_post_comment",
        "vote_post",
        "vote_post_comment",
        "vote_question",
        "vote_answer",
        "reaction_post",
        "reaction_post_comment",
        "reaction_question",
        "reaction_answer",
        "reaction_answer_comment",
    ]
    pagination = get_all_user_actions_by_commons_and_action_types(
        **commons.dict(), action_types=action_types
    )

    if request.headers.get("Hx-Request") == "true":
        template = "/user/activity/list.html.jinja"
    else:
        template = "/user/activity/index.html.jinja"

    return render_template(template, pagination=pagination, commons=commons)


@bp_user.route("/me/activity/questions-and-posts", methods=[HTTPMethod.GET])
@login_required
def my_activity_about_question_and_post():
    """
    (GET) Show my activity about questions and posts.
    """

    commons = CommonParameters(**request.args.to_dict())
    commons.filters = f"user_id-eq-{current_user.id}"

    pagination = get_all_user_actions_by_commons_and_action_types(
        **commons.dict(), action_types=["create_post", "create_question"]
    )

    return render_template(
        "/user/activity/index.html.jinja",
        pagination=pagination,
    )


@bp_user.route("/me/activity/answers-and-comments", methods=[HTTPMethod.GET])
@login_required
def my_activity_about_answer_and_comment():
    """
    (GET) Show my activity about answers and comments.
    """

    commons = CommonParameters(**request.args.to_dict())
    commons.filters = f"user_id-eq-{current_user.id}"

    pagination = get_all_user_actions_by_commons_and_action_types(
        **commons.dict(),
        action_types=["create_answer", "create_answer_comment", "create_post_comment"],
    )

    return render_template(
        "/user/activity/index.html.jinja", pagination=pagination, commons=commons
    )


@bp_user.route("/me/activity/votes", methods=[HTTPMethod.GET])
@login_required
def my_activity_about_voting():
    """
    (GET) Show my activity about voting page.
    """

    commons = CommonParameters(**request.args.to_dict())
    commons.filters = f"user_id-eq-{current_user.id}"

    pagination = get_all_user_actions_by_commons_and_action_types(
        **commons.dict(),
        action_types=["vote_post", "vote_post_comment", "vote_question", "vote_answer"],
    )

    if request.headers.get("Hx-Request") == "true":
        template = "/user/activity/votes/list.html.jinja"
    else:
        template = "/user/activity/votes/index.html.jinja"

    return render_template(template, pagination=pagination, commons=commons)


@bp_user.route("/me/activity/reactions", methods=[HTTPMethod.GET])
@login_required
def my_activity_about_reaction():
    """
    (GET) Show my activity about reaction page.
    """

    commons = CommonParameters(**request.args.to_dict())
    commons.filters = f"user_id-eq-{current_user.id}"

    pagination = get_all_user_actions_by_commons_and_action_types(
        **commons.dict(),
        action_types=[
            "reaction_post",
            "reaction_post_comment",
            "reaction_question",
            "reaction_answer",
            "reaction_answer_comment",
        ],
    )

    if request.headers.get("Hx-Request") == "true":
        template = "/user/activity/reactions/list.html.jinja"
    else:
        template = "/user/activity/reactions/index.html.jinja"

    return render_template(template, pagination=pagination, commons=commons)
