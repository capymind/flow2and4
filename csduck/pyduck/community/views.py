"""
This is the module for handling requests related to pyduck community.
"""

from datetime import timezone, datetime
import json
import os
import uuid
import logging
from pydantic import ValidationError
from flask import Blueprint, render_template, request, url_for, redirect, abort
from flask_login import login_required, current_user
from http import HTTPStatus, HTTPMethod
from csduck.pyduck.community.schemas import (
    QuestionImageUploadCreate,
    QuestionCreate,
    QuestionTagCreate,
    QuestionUpdate,
    QuestionVoteCreate,
)
from werkzeug.utils import secure_filename
from csduck.pyduck.community.service import (
    create_question_image_upload,
    create_question,
    get_or_create_tags,
    get_all_questions_by_commons,
    get_question,
    update_question_adding_history,
    create_question_vote
)
from csduck.pyduck.schemas import CommonParameters
from csduck.database import db

logger = logging.getLogger(__name__)

bp = Blueprint(
    "community",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/community",
)


@bp.route("/<category>")
def index(category: str):
    """Show community page by category."""

    if category == "help":
        commons = CommonParameters(**request.args.to_dict(flat=False))

        question_pagination = get_all_questions_by_commons(**commons.dict())

        return render_template(
            "community/index_help.html.jinja", question_pagination=question_pagination
        )

    return render_template("community/index.html.jinja")


@bp.route(
    "/questions/<int:question_id>",
    methods=[HTTPMethod.GET, HTTPMethod.DELETE, HTTPMethod.PUT],
)
def question(question_id: int):
    """
    (GET) Show question page.
    """

    q = get_question(question_id=question_id)
    if q is None:
        abort(HTTPStatus.NOT_FOUND)

    return render_template("community/question/question.html.jinja", q=q)


@bp.route(
    "/questions/<int:question_id>/edit", methods=[HTTPMethod.GET, HTTPMethod.POST]
)
@login_required
def question_edit(question_id: int):
    """
    (GET) Show question edit page.
    (POST) Process question edit.
    """

    q_old = get_question(question_id=question_id)
    if q_old is None:
        abort(HTTPStatus.NOT_FOUND)

    if q_old.user_id != current_user.id:
        abort(HTTPStatus.UNAUTHORIZED)

    if request.method == HTTPMethod.POST:
        tags_dict = request.form.get("tags")
        if tags_dict:
            tags_in = [tag.get("value") for tag in json.loads(tags_dict)]
            tags_in = get_or_create_tags(tags_in=tags_in)

        question_in = None
        try:
            question_in = QuestionUpdate(
                **request.form.to_dict(),
                id=q_old.id,
                user_id=current_user.id,
                updated_at=datetime.now(timezone.utc)
            )

        except ValidationError as e:
            logger.warn(e)

        question = update_question_adding_history(
            question_in=question_in, tags_in=tags_in
        )

        return redirect(url_for("pyduck.community.question", question_id=question.id))

    return render_template("community/question/edit.html.jinja", q=q_old)


@bp.route("/questions/<int:question_id>/vote", methods=[HTTPMethod.POST])
@login_required
def question_vote(question_id: int):
    """
    (POST) Process vote and return fragment.
    """

    q = get_question(question_id=question_id)
    if q is None:
        abort(HTTPStatus.NOT_FOUND)

    vote_in = QuestionVoteCreate(user_id=current_user.id, question_id=question_id)
    create_question_vote(vote_in=vote_in)



@bp.route("/help/new", methods=[HTTPMethod.GET, HTTPMethod.POST])
@login_required
def question_new():
    """
    (GET) Show new question page.
    (POST) Process new question.
    """

    if request.method == HTTPMethod.POST:
        tags_dict = request.form.get("tags")
        if tags_dict:
            tags_in = [tag.get("value") for tag in json.loads(tags_dict)]
            tags_in = get_or_create_tags(tags_in=tags_in)

        question_in = None
        try:
            question_in = QuestionCreate(
                **request.form.to_dict(), user_id=current_user.id
            )
        except ValidationError as e:
            logger.warn(e.errors)
            return render_template("community/question/new.html.jinja")

        create_question(question_in=question_in, tags_in=tags_in)
        return redirect(url_for("pyduck.community.index", category="help"))

    return render_template("community/question/new.html.jinja")


@bp.route("/<category>/new", methods=[HTTPMethod.GET, HTTPMethod.POST])
def post(category: str):
    """
    (GET) Show new post page.
    (POST) Process new post.
    """

    if request.method == HTTPMethod.POST:
        ...

    return render_template("community/post/new.html.jinja")


@bp.route("/<category>/upload/images", methods=[HTTPMethod.POST])
@login_required
def image_upload(category: str):
    """Process upload image by editor."""

    file = request.files.get("upload")

    if file is None:
        return {"error": {"message": "파일이 존재하지 않습니다."}}

    original_filename = secure_filename(file.filename)
    format_ = original_filename.rsplit(".", maxsplit=1)[1]

    if format_.lower() not in ["jpg", "jpeg", "png", "gif", "webp"]:
        return {"error": {"message": "지원하는 이미지 파일형식이 아닙니다."}}

    filename = uuid.uuid4().hex + "." + format_
    folder = "pyduck/community/static/upload/images"

    file.save(os.path.join(folder, filename))
    filesize = os.stat(os.path.join(folder, filename)).st_size
    mimetype = file.mimetype

    upload_in = QuestionImageUploadCreate(
        user_id=current_user.id,
        url=url_for("pyduck.community.static", filename="upload/images/" + filename),
        filename=filename,
        original_filename=original_filename,
        mimetype=mimetype,
        filesize=filesize,
    )

    upload = create_question_image_upload(upload_in=upload_in)

    return {"url": upload.url}
