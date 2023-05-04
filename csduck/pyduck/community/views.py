"""
This is the module for handling requests related to pyduck community.
"""

from datetime import timezone, datetime
import json
import os
import uuid
import logging
from pydantic import ValidationError
from flask import (
    Blueprint,
    render_template,
    request,
    url_for,
    redirect,
    abort,
    get_template_attribute,
    make_response,
)
from flask_login import login_required, current_user
from http import HTTPStatus, HTTPMethod
from csduck.pyduck.community.schemas import (
    QuestionImageUploadCreate,
    QuestionCreate,
    QuestionTagCreate,
    QuestionUpdate,
    QuestionVoteCreate,
    QuestionReactionCreate,
    AnswerCreate,
    AnswerUpdate,
    AnswerVoteCreate,
    AnswerReactionCreate,
    AnswerCommentCreate,
    AnswerCommentUpdate,
    AnswerCommentReactionCreate,
)
from werkzeug.utils import secure_filename
from csduck.pyduck.community.service import (
    create_question_image_upload,
    create_question,
    get_or_create_tags,
    get_all_questions_by_commons,
    get_question,
    update_question_adding_history,
    create_question_vote,
    get_question_vote,
    delete_question_vote,
    create_question_reaction,
    get_question_reaction,
    delete_question_reaction,
    create_answer,
    get_answer,
    create_answer_vote,
    get_answer_vote,
    delete_answer_vote,
    create_answer_reaction,
    get_answer_reaction,
    delete_answer_reaction,
    get_all_answers_by_commons,
    update_answer_adding_history,
    create_answer_comment,
    get_comment,
    get_answer_comment_reaction,
    delete_answer_comment_reaction,
    create_answer_comment_reaction,
    update_answer_comment_adding_history,
    mark_answer_as_answered,
    mark_answer_as_unanswered,
    get_all_answer_comments_by_commons,
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

        qp = get_all_questions_by_commons(**commons.dict())

        return render_template("community/index_help.html.jinja", qp=qp)

    return render_template("community/index.html.jinja")


@bp.route("/questions", methods=[HTTPMethod.GET])
def questions():
    """
    (GET) Show questions fragment.
    """

    commons = CommonParameters(**request.args.to_dict())
    qp = get_all_questions_by_commons(**commons.dict())
    print(qp.total, qp.items)

    return render_template("community/question/questions.html.jinja", qp=qp)


@bp.route(
    "/questions/<int:question_id>",
    methods=[HTTPMethod.GET, HTTPMethod.DELETE],
)
def question(question_id: int):
    """
    (GET) Show question page.
    """

    q = get_question(question_id=question_id)
    if q is None:
        abort(HTTPStatus.NOT_FOUND)

    commons = CommonParameters(**request.args.to_dict(flat=False))
    ap = get_all_answers_by_commons(**commons.dict(), question_id=question_id)

    return render_template("community/question/question.html.jinja", q=q, ap=ap)


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


@bp.route(
    "/questions/<int:question_id>/reactions",
    methods=[HTTPMethod.POST],
)
@login_required
def question_reaction(question_id: int):
    """
    (POST) Process reaction or unreaction and return fragment.
    """

    q = get_question(question_id=question_id)
    if q is None:
        abort(HTTPStatus.NOT_FOUND)

    action, code = request.form.get("action").split()

    # HACK: hard-coded.
    if code not in [
        "thumbs_up",
        "thumbs_down",
        "heart",
        "tada",
        "smile",
        "sweat",
        "sweat",
        "eyes",
    ]:
        abort(HTTPStatus.BAD_REQUEST)

    r = get_question_reaction(question_id=q.id, user_id=current_user.id, code=code)

    if action == "react":
        if r is not None:
            abort(HTTPStatus.UNPROCESSABLE_ENTITY)
        reaction_in = QuestionReactionCreate(
            user_id=current_user.id, question_id=question_id, code=code
        )
        question = create_question_reaction(reaction_in=reaction_in)
        return render_template(
            "community/question/reaction.html.jinja", question=question
        )

    if action == "unreact":
        if r is None:
            abort(HTTPStatus.UNPROCESSABLE_ENTITY)
        question = delete_question_reaction(
            question_id=question_id, user_id=current_user.id, code=code
        )
        return render_template(
            "community/question/reaction.html.jinja", question=question
        )


@bp.route(
    "/questions/<int:question_id>/vote", methods=[HTTPMethod.POST, HTTPMethod.DELETE]
)
@login_required
def question_vote(question_id: int):
    """
    (POST) Process vote and return fragment.
    (DELETE) Process unvote and return fragment.
    """

    render_vote = get_template_attribute(
        "community/question/render_vote.html.jinja", "render_vote"
    )

    q = get_question(question_id=question_id)
    if q is None:
        abort(HTTPStatus.NOT_FOUND)

    if request.method == HTTPMethod.POST:
        vote_in = QuestionVoteCreate(user_id=current_user.id, question_id=question_id)
        question = create_question_vote(vote_in=vote_in)
        return render_vote(question=question, voted=True)

    if request.method == HTTPMethod.DELETE:
        vote = get_question_vote(question_id=question_id, user_id=current_user.id)

        if vote is None:
            abort(HTTPStatus.BAD_REQUEST)
        question = delete_question_vote(
            question_id=question_id, user_id=current_user.id
        )
        return render_vote(question=question, voted=False)


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


@bp.route("/answers", methods=[HTTPMethod.POST, HTTPMethod.PUT])
@login_required
def answer():
    """
    (POST) Process answer creation to question.
    (PUT) Process answer modification to question.
    """

    if request.method == HTTPMethod.POST:
        answer_in = None
        try:
            answer_in = AnswerCreate(**request.form.to_dict(), user_id=current_user.id)
        except ValidationError as e:
            logger.warn(e.errors())
            abort(HTTPStatus.BAD_REQUEST)

        answer = create_answer(answer_in=answer_in)

        res = make_response(
            render_template("community/answer/answer.html.jinja", answer=answer)
        )
        res.headers["HX-Trigger-After-Settle"] = "answer-created"

    if request.method == HTTPMethod.PUT:
        answer_id = request.form.get("answer_id")
        content = request.form.get("content")

        if answer_id is None or content is None:
            abort(HTTPStatus.BAD_REQUEST)

        answer = get_answer(answer_id=answer_id)
        if answer is None:
            abort(HTTPStatus.BAD_REQUEST)

        try:
            answer_in = AnswerUpdate(
                **answer.dict(exclude={"content", "updated_at"}),
                content=content,
                updated_at=datetime.now(timezone.utc)
            )
        except ValidationError as e:
            logger.warn(e.errors())

        answer = update_answer_adding_history(answer_in=answer_in)
        res = make_response(
            render_template("community/answer/answer.html.jinja", answer=answer)
        )

    return res


@bp.route("/answers/<int:answer_id>/vote", methods=[HTTPMethod.POST, HTTPMethod.DELETE])
@login_required
def answer_vote(answer_id: int):
    """
    (POST) Process vote and return fragment.
    (DELETE) Process unvote and return fragment.
    """

    render_vote = get_template_attribute(
        "community/answer/render_vote.html.jinja", "render_vote"
    )

    a = get_answer(answer_id=answer_id)
    if a is None:
        abort(HTTPStatus.NOT_FOUND)

    if request.method == HTTPMethod.POST:
        vote_in = AnswerVoteCreate(user_id=current_user.id, answer_id=answer_id)
        answer = create_answer_vote(vote_in=vote_in)
        return render_vote(answer=answer, voted=True)

    if request.method == HTTPMethod.DELETE:
        vote = get_answer_vote(answer_id=answer_id, user_id=current_user.id)

        if vote is None:
            abort(HTTPStatus.BAD_REQUEST)
        answer = delete_answer_vote(answer_id=answer_id, user_id=current_user.id)
        return render_vote(answer=answer, voted=False)


@bp.route(
    "/answers/<int:answer_id>/reactions",
    methods=[HTTPMethod.POST],
)
@login_required
def answer_reaction(answer_id: int):
    """
    (POST) Process reaction or unreaction and return fragment.
    """

    a = get_answer(answer_id=answer_id)
    if a is None:
        abort(HTTPStatus.NOT_FOUND)

    action, code = request.form.get("action").split()

    # HACK: hard-coded.
    if code not in [
        "thumbs_up",
        "thumbs_down",
        "heart",
        "tada",
        "smile",
        "sweat",
        "sweat",
        "eyes",
    ]:
        abort(HTTPStatus.BAD_REQUEST)

    r = get_answer_reaction(answer_id=a.id, user_id=current_user.id, code=code)

    if action == "react":
        if r is not None:
            abort(HTTPStatus.UNPROCESSABLE_ENTITY)
        reaction_in = AnswerReactionCreate(
            user_id=current_user.id, answer_id=answer_id, code=code
        )
        answer = create_answer_reaction(reaction_in=reaction_in)
        return render_template("community/answer/reaction.html.jinja", answer=answer)

    if action == "unreact":
        if r is None:
            abort(HTTPStatus.UNPROCESSABLE_ENTITY)
        answer = delete_answer_reaction(
            answer_id=answer_id, user_id=current_user.id, code=code
        )
        return render_template("community/answer/reaction.html.jinja", answer=answer)


@bp.route("/answers/<int:answer_id>/comments", methods=[HTTPMethod.GET])
def comments(answer_id: int):
    """
    (GET) Show comments to specific answer.
    """

    commons = CommonParameters(**request.args.to_dict())
    cp = get_all_answer_comments_by_commons(**commons.dict(), answer_id=answer_id)

    return render_template("community/answer_comment/answer_comments.html.jinja", cp=cp)


@bp.route("/comments", methods=[HTTPMethod.POST, HTTPMethod.PUT])
@login_required
def comment_to_answer():
    """
    (POST) Process comment creation to question's answer.
    (PUT) Process comment modification to qeustion's answer.
    """

    if request.method == HTTPMethod.POST:
        comment_in = None
        try:
            comment_in = AnswerCommentCreate(
                **request.form.to_dict(), user_id=current_user.id
            )
        except ValidationError as e:
            logger.warn(e.errors())
            abort(HTTPStatus.BAD_REQUEST)

        comment = create_answer_comment(comment_in=comment_in)

        res = make_response(
            render_template(
                "community/answer_comment/answer_comment.html.jinja", comment=comment
            )
        )
        res.headers["HX-Trigger-After-Settle"] = "comment-created"

    if request.method == HTTPMethod.PUT:
        comment_id = request.form.get("comment_id")
        content = request.form.get("content")
        if comment_id is None or content is None:
            abort(HTTPStatus.BAD_REQUEST)

        comment = get_comment(comment_id=comment_id)
        if comment is None:
            abort(HTTPStatus.BAD_REQUEST)
        if comment.user_id != current_user.id:
            abort(HTTPStatus.UNAUTHORIZED)

        try:
            comment_in = AnswerCommentUpdate(
                **comment.dict(exclude={"content", "updated_at"}),
                content=content,
                updated_at=datetime.now(timezone.utc)
            )
        except ValidationError as e:
            logger.warn(e.errors())

        comment = update_answer_comment_adding_history(comment_in=comment_in)
        res = make_response(
            render_template(
                "community/answer_comment/answer_comment.html.jinja", comment=comment
            )
        )

    return res


@bp.route(
    "/comments/<int:comment_id>/reactions",
    methods=[HTTPMethod.POST],
)
@login_required
def answer_comment_reaction(comment_id: int):
    """
    (POST) Process reaction or unreaction and return fragment.
    """

    comment = get_comment(comment_id=comment_id)
    if comment is None:
        abort(HTTPStatus.NOT_FOUND)

    action, code = request.form.get("action").split()

    # HACK: hard-coded.
    if code not in [
        "thumbs_up",
        "thumbs_down",
        "heart",
        "tada",
        "smile",
        "sweat",
        "sweat",
        "eyes",
    ]:
        abort(HTTPStatus.BAD_REQUEST)

    r = get_answer_comment_reaction(
        comment_id=comment.id, user_id=current_user.id, code=code
    )

    if action == "react":
        if r is not None:
            abort(HTTPStatus.UNPROCESSABLE_ENTITY)
        reaction_in = AnswerCommentReactionCreate(
            user_id=current_user.id, comment_id=comment_id, code=code
        )
        comment = create_answer_comment_reaction(reaction_in=reaction_in)
        return render_template(
            "community/answer_comment/reaction.html.jinja", comment=comment
        )

    if action == "unreact":
        if r is None:
            abort(HTTPStatus.UNPROCESSABLE_ENTITY)
        comment = delete_answer_comment_reaction(
            comment_id=comment_id, user_id=current_user.id, code=code
        )
        return render_template(
            "community/answer_comment/reaction.html.jinja", comment=comment
        )


@bp.route("/questions/<int:question_id>/answers", methods=[HTTPMethod.GET])
def answers(question_id: int):
    """
    (GET) Show answers fragment.
    """

    commons = CommonParameters(**request.args.to_dict())

    answers = get_all_answers_by_commons(**commons.dict(), question_id=question_id)

    return render_template("community/answer/answers.html.jinja", answers=answers)


@bp.route("/answers/<int:answer_id>/answered", methods=[HTTPMethod.PUT])
def answered(answer_id: int):
    """
    (PUT) mark specific answer as answered and return relevant fragment.
    """

    answer = get_answer(answer_id=answer_id)

    if answer is None:
        abort(HTTPStatus.NOT_FOUND)

    answer = mark_answer_as_answered(answer_id=answer.id)

    res = make_response(
        render_template("community/answer/answer.html.jinja", answer=answer)
    )
    res.headers["HX-Trigger"] = "question-answered"

    return res


@bp.route("/answers/<int:answer_id>/unanswered", methods=[HTTPMethod.PUT])
def unanswered(answer_id: int):
    """
    (PUT) mark specific answer as unanswered and return relevant fragment.
    """

    answer = get_answer(answer_id=answer_id)

    if answer is None:
        abort(HTTPStatus.NOT_FOUND)

    answer = mark_answer_as_unanswered(answer_id=answer.id)

    res = make_response(
        render_template("community/answer/answer.html.jinja", answer=answer)
    )
    res.headers["HX-Trigger"] = "question-answered"

    return res
