"""
This is the module for handling requests related to pyduck community.


[ route handlers ]
/<category>                                                                     -> index
/<category>/posts                                                               -> posts
/questions                                                                      -> questions
/questions/<int:question_id>                                                    -> question
/<category/posts/<int:post_id>                                                  -> post
/posts/<int:post_id>                                                            -> post
/questions/<int:question_id>/edit                                               -> question_edit
/posts/<int:post_id>/edit                                                       -> post_edit
/questsions/<int:question_id>/reactions                                         -> questions_reaction
/posts/<int:post_id>/reactions                                                  -> post_reaction
/posts/<int:post_id>/comments/<int:post_comment_id>/reactions                   -> post_comment_reaction
/questsions/<int:question_id>/vote                                              -> question_vote
/posts/<int:post_id>/vote                                                       -> post_vote
/help/new                                                                       -> question_new
/<category>/new                                                                 -> post_new
/<category>/upload/images                                                       -> image_upload
/answers                                                                        -> answer
/posts/<int:post_id>/comments                                                   -> post_comment
/posts/<int:post_id>/comments/<int:post_comment_id>                             -> post_comment
/answers/<int:answer_id>/vote                                                   -> answer_vote
/answers/<int:answer_id>/reactions                                              -> answer_reaction
/answeres/<int:answer_id>/comments                                              -> comments
/posts/<int:post_id>/comments                                                   -> comments_to_post
/posts/<int:post_id>/comments/<int:post_comment_id>/comments                    -> comment_to_post_comment
/posts/<int:post_id>/comments/<int:post_comment_id>/comments/<int:comment_id>   -> comment_to_post_comment
/posts/<int:post_id>/comments/<int:post_comment_id>/comments                    -> comments_to_post_comment
/answers/<int:answer_id>/comments                                               -> comment_to_answer
/answers/<int:answer_id>/comments/<int:answer_comment_id>                       -> comment_to_answer
/comments/<int:answer_comment_id>/reactions                                     -> answer_comment_reaction
/questions/<int:question_id>/answers                                            -> answeres
/answers/<int:answer_id>/answered                                               -> answered
/answers/<int:answer_id>/unanswered                                             -> unanswered
/comments/<int:post_comment_id>/vote                                            -> post_comment_vote
"""

import json
import logging
import os
import uuid
from datetime import date, datetime, timedelta, timezone
from http import HTTPMethod, HTTPStatus

from flask import (
    Blueprint,
    abort,
    get_template_attribute,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required
from pydantic import ValidationError
from werkzeug.utils import secure_filename

from flow2and4.database import db
from flow2and4.pyduck.auth.schemas import (
    UserActionCreateAnswerCommentCreate,
    UserActionCreateAnswerCreate,
    UserActionCreatePostCommentCreate,
    UserActionCreatePostCreate,
    UserActionCreateQuestionCreate,
    UserActionReactionAnswerCommentCreate,
    UserActionReactionAnswerCreate,
    UserActionReactionPostCommentCreate,
    UserActionReactionPostCreate,
    UserActionReactionQuestionCreate,
    UserActionVoteAnswerCreate,
    UserActionVotePostCommentCreate,
    UserActionVotePostCreate,
    UserActionVoteQuestionCreate,
)
from flow2and4.pyduck.auth.service import create_user_action, delete_user_action
from flow2and4.pyduck.community.helpers import date_filters
from flow2and4.pyduck.community.schemas import (
    AnswerCommentCreate,
    AnswerCommentReactionCreate,
    AnswerCommentUpdate,
    AnswerCreate,
    AnswerReactionCreate,
    AnswerUpdate,
    AnswerVoteCreate,
    PostCommentCreate,
    PostCommentHistoryCreate,
    PostCommentReactionCreate,
    PostCommentUpdate,
    PostCommentVoteCreate,
    PostCreate,
    PostHistoryCreate,
    PostReactionCreate,
    PostUpdate,
    PostVoteCreate,
    QuestionCreate,
    QuestionImageUploadCreate,
    QuestionReactionCreate,
    QuestionTagCreate,
    QuestionUpdate,
    QuestionVoteCreate,
)
from flow2and4.pyduck.community.service import (
    create_answer,
    create_answer_comment,
    create_answer_comment_reaction,
    create_answer_reaction,
    create_answer_vote,
    create_comment_to_post_comment,
    create_post,
    create_post_comment,
    create_post_comment_reaction,
    create_post_comment_vote,
    create_post_reaction,
    create_post_vote,
    create_question,
    create_question_image_upload,
    create_question_reaction,
    create_question_vote,
    delete_answer,
    delete_answer_comment_reaction,
    delete_answer_reaction,
    delete_answer_vote,
    delete_comment_to_post_comment,
    delete_post,
    delete_post_comment,
    delete_post_comment_reaction,
    delete_post_comment_vote,
    delete_post_reaction,
    delete_post_vote,
    delete_question_reaction,
    delete_question_vote,
    get_all_answer_comments_by_commons,
    get_all_answers_by_commons,
    get_all_comments_to_post_by_commons,
    get_all_comments_to_post_comment_by_commons,
    get_all_posts_by_commons_and_category,
    get_all_questions_by_commons,
    get_answer,
    get_answer_comment,
    get_answer_comment_reaction,
    get_answer_reaction,
    get_answer_vote,
    get_comment_to_post_comment,
    get_or_create_post_tags,
    get_or_create_tags,
    get_post,
    get_post_comment,
    get_post_comment_reaction,
    get_post_comment_vote,
    get_post_reaction,
    get_post_vote,
    get_question,
    get_question_reaction,
    get_question_vote,
    mark_answer_as_answered,
    mark_answer_as_unanswered,
    update_answer_adding_history,
    update_answer_comment_adding_history,
    update_post_adding_history,
    update_post_comment_adding_history,
    update_question_adding_history,
)
from flow2and4.pyduck.notification.schemas import (
    NotificationForAnswerCommentCreate,
    NotificationForAnswerCommentReactionCreate,
    NotificationForAnswerCreate,
    NotificationForAnswerReactionCreate,
    NotificationForAnswerVoteCreate,
    NotificationForPostCommentCreate,
    NotificationForPostCommentReactionCreate,
    NotificationForPostCommentVoteCreate,
    NotificationForPostReactionCreate,
    NotificationForPostVoteCreate,
    NotificationForQuestionReactionCreate,
    NotificationForQuestionVoteCreate,
)
from flow2and4.pyduck.notification.service import (
    create_notification,
    delete_notification,
)
from flow2and4.pyduck.schemas import CommonParameters

logger = logging.getLogger(__name__)

bp = Blueprint(
    "community",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/community",
)

VALID_REACTION_CODE = {
    "thumbs_up",
    "thumbs_down",
    "heart",
    "tada",
    "smile",
    "sweat",
    "sweat",
    "eyes",
}


@bp.route("/<category>")
def index(category: str):
    """Show community page by category."""

    commons = CommonParameters(**request.args.to_dict())

    if category == "help":
        qp = get_all_questions_by_commons(**commons.dict())

        return render_template(
            "community/index/index_help.html.jinja", qp=qp, date_filters=date_filters
        )

    else:
        post_pagination = get_all_posts_by_commons_and_category(
            **commons.dict(), category=category
        )

        return render_template(
            f"community/index/index.html.jinja",
            post_pagination=post_pagination,
            date_filters=date_filters,
            category=category,
            commons=commons,
        )

    return render_template("community/index.html.jinja")


@bp.route("/<category>/posts", methods=[HTTPMethod.GET])
def posts(category: str):
    """
    (GET) Show posts given category fragment.
    -> infinite scroll item list
    """

    commons = CommonParameters(**request.args.to_dict())
    post_pagination = get_all_posts_by_commons_and_category(
        category=category, **commons.dict()
    )

    return render_template(
        "community/post/posts.html.jinja",
        post_pagination=post_pagination,
        category=category,
        commons=commons,
    )


@bp.route("/questions", methods=[HTTPMethod.GET])
def questions():
    """
    (GET) Show questions fragment.
    -> infinite scroll item list
    """

    commons = CommonParameters(**request.args.to_dict())
    qp = get_all_questions_by_commons(**commons.dict())

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
    "/posts/<int:post_id>",
    methods=[HTTPMethod.GET, HTTPMethod.DELETE],
)
@bp.route(
    "/<category>/posts/<int:post_id>",
    methods=[HTTPMethod.GET, HTTPMethod.DELETE],
)
def post(post_id: int, category: str | None = None):
    """
    (GET) Show post page.
    (DELETE) Delete post and redirect post list.
    """

    post = get_post(post_id=post_id)
    if post is None:
        abort(HTTPStatus.NOT_FOUND)

    commons = CommonParameters(**request.args.to_dict())
    post_comment_pagination = get_all_comments_to_post_by_commons(
        **commons.dict(), post_id=post_id
    )

    if request.method == HTTPMethod.DELETE:
        if current_user.id != post.user_id:
            abort(HTTPStatus.UNAUTHORIZED)

        delete_post(post_id=post.id)

        res = make_response()
        res.headers["HX-Redirect"] = url_for(
            "pyduck.community.index", category=post.category
        )

        return res

    return render_template(
        "community/post/post.html.jinja",
        post=post,
        post_comment_pagination=post_comment_pagination,
    )


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
        tags_in = []
        if tags_dict:
            tags_in = [tag.get("value") for tag in json.loads(tags_dict)]
            tags_in = get_or_create_tags(tags_in=tags_in)

        question_in = None
        try:
            question_in = QuestionUpdate(
                **request.form.to_dict(),
                id=q_old.id,
                user_id=current_user.id,
                updated_at=datetime.now(timezone.utc),
            )

        except ValidationError as e:
            logger.warn(e)

        question = update_question_adding_history(
            question_in=question_in, tags_in=tags_in
        )

        return redirect(url_for("pyduck.community.question", question_id=question.id))

    return render_template("community/question/edit.html.jinja", q=q_old)


@bp.route("/posts/<int:post_id>/edit", methods=[HTTPMethod.GET, HTTPMethod.POST])
@login_required
def post_edit(post_id: int):
    """
    (GET) Show post edit page.
    (POST) Process post edit.
    """

    post_old = get_post(post_id=post_id)
    if post_old is None:
        abort(HTTPStatus.NOT_FOUND)

    if post_old.user_id != current_user.id:
        abort(HTTPStatus.UNAUTHORIZED)

    if request.method == HTTPMethod.POST:
        tags_dict = request.form.get("tags")
        tags_in = []
        if tags_dict:
            tags_in = [tag.get("value") for tag in json.loads(tags_dict)]
            tags_in = get_or_create_post_tags(tags_in=tags_in)

        post_in = None
        try:
            post_in = PostUpdate(
                **request.form.to_dict(),
                id=post_old.id,
                category=post_old.category,
                user_id=current_user.id,
                updated_at=datetime.now(timezone.utc),
            )

        except ValidationError as e:
            logger.warn(e)

        post = update_post_adding_history(post_in=post_in, tags_in=tags_in)

        return redirect(url_for("pyduck.community.post", post_id=post.id))

    return render_template("community/post/edit.html.jinja", post=post_old)


@bp.route(
    "/questions/<int:question_id>/reactions",
    methods=[HTTPMethod.POST],
)
@login_required
def question_reaction(question_id: int):
    """
    (POST) Process reaction or unreaction to question and return fragment.
    """

    action, code = request.form.get("action").split()

    if code not in VALID_REACTION_CODE:
        abort(HTTPStatus.BAD_REQUEST)

    reaction = get_question_reaction(
        question_id=question_id, user_id=current_user.id, code=code
    )

    if action == "react":
        if reaction is not None:
            abort(HTTPStatus.CONFLICT)
        reaction_in = QuestionReactionCreate(
            user_id=current_user.id, target_id=question_id, code=code
        )
        question = create_question_reaction(reaction_in=reaction_in)

        # user action.
        user_action_in = UserActionReactionQuestionCreate(
            user_id=current_user.id, target_id=question.id, action_value=code
        )
        user_action = create_user_action(user_action_in=user_action_in)

        # notification.
        if question.user_id != user_action.user_id:
            notification_in = NotificationForQuestionReactionCreate(
                user_id=question.user_id,
                notification_value=code,
                notification_target_id=question.id,
                from_user_id=current_user.id,
                to_user_id=question.user_id,
            )
            create_notification(notification_in=notification_in)

    if action == "unreact":
        if reaction is None:
            abort(HTTPStatus.NOT_FOUND)
        question = delete_question_reaction(
            question_id=question_id, user_id=current_user.id, code=code
        )

        # user action.
        delete_user_action(
            user_id=current_user.id,
            action_type="reaction_question",
            target_id=question.id,
            action_value=code,
        )

        # notification.
        if question.user_id != current_user.id:
            delete_notification(
                user_id=question.user_id,
                notification_type="reaction_question",
                notification_target_id=question.id,
                from_user_id=current_user.id,
                to_user_id=question.user.id,
                notification_value=code,
            )

    return render_template("community/question/reaction.html.jinja", question=question)


@bp.route(
    "/posts/<int:post_id>/reactions",
    methods=[HTTPMethod.POST],
)
@login_required
def post_reaction(post_id: int):
    """
    (POST) Process reaction or unreaction to post and return fragment.

    -----
    [model flow]
    """

    action, code = request.form.get("action").split()

    if code not in VALID_REACTION_CODE:
        abort(HTTPStatus.BAD_REQUEST)

    reaction = get_post_reaction(post_id=post_id, user_id=current_user.id, code=code)

    if action == "react":
        if reaction is not None:
            abort(HTTPStatus.CONFLICT)

        reaction_in = PostReactionCreate(
            user_id=current_user.id, target_id=post_id, code=code
        )
        post = create_post_reaction(reaction_in=reaction_in)

        # user action.
        user_action_in = UserActionReactionPostCreate(
            user_id=current_user.id, target_id=post.id, action_value=code
        )
        user_action = create_user_action(user_action_in=user_action_in)

        # notification.
        if post.user_id != user_action.user_id:
            notification_in = NotificationForPostReactionCreate(
                user_id=post.user_id,
                notification_value=code,
                notification_target_id=post.id,
                from_user_id=current_user.id,
                to_user_id=post.user_id,
            )
            create_notification(notification_in=notification_in)

    if action == "unreact":
        if reaction is None:
            abort(HTTPStatus.NOT_FOUND)

        post = delete_post_reaction(post_id=post_id, user_id=current_user.id, code=code)

        # user action.
        delete_user_action(
            user_id=current_user.id,
            action_type="reaction_post",
            target_id=post.id,
            action_value=code,
        )

        # notification.
        if post.user_id != current_user.id:
            delete_notification(
                user_id=post.user_id,
                notification_type="reaction_post",
                notification_target_id=post.id,
                notification_value=code,
                from_user_id=current_user.id,
                to_user_id=post.user_id,
            )

    return render_template("community/post/reaction.html.jinja", post=post)


@bp.route(
    "/posts/<int:post_id>/comments/<int:post_comment_id>/reactions",
    methods=[HTTPMethod.POST],
)
@login_required
def post_comment_reaction(post_id: int, post_comment_id: int):
    """
    (POST) Process reaction or unreaction and return fragment.
    """

    action, code = request.form.get("action").split()

    if code not in VALID_REACTION_CODE:
        abort(HTTPStatus.BAD_REQUEST)

    reaction = get_post_comment_reaction(
        post_comment_id=post_comment_id, user_id=current_user.id, code=code
    )

    if action == "react":
        if reaction is not None:
            abort(HTTPStatus.CONFLICT)

        reaction_in = PostCommentReactionCreate(
            user_id=current_user.id, target_id=post_comment_id, code=code
        )
        post_comment = create_post_comment_reaction(reaction_in=reaction_in)

        # user action.
        user_action_in = UserActionReactionPostCommentCreate(
            user_id=current_user.id, target_id=post_comment.id, action_value=code
        )
        user_action = create_user_action(user_action_in=user_action_in)

        # notification.
        if post_comment.user_id != user_action.user_id:
            notification_in = NotificationForPostCommentReactionCreate(
                user_id=post_comment.user_id,
                notification_value=code,
                notification_target_id=post_comment.id,
                from_user_id=current_user.id,
                to_user_id=post_comment.user_id,
            )
            create_notification(notification_in=notification_in)

    if action == "unreact":
        if reaction is None:
            abort(HTTPStatus.NOT_FOUND)

        post_comment = delete_post_comment_reaction(
            post_comment_id=post_comment_id, user_id=current_user.id, code=code
        )

        # user action.
        delete_user_action(
            user_id=current_user.id,
            action_type="reaction_post_comment",
            target_id=post_comment.id,
            action_value=code,
        )

        # notification.
        if post_comment.user_id != current_user.id:
            delete_notification(
                user_id=post_comment.user_id,
                notification_type="reaction_post_comment",
                notification_target_id=post_comment.id,
                notification_value=code,
                from_user_id=current_user.id,
                to_user_id=post_comment.user_id,
            )

    return render_template(
        "community/post_comment/reaction.html.jinja", post_comment=post_comment
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

    vote = get_question_vote(question_id=question_id, user_id=current_user.id)

    if request.method == HTTPMethod.POST:
        if vote is not None:
            abort(HTTPStatus.CONFLICT)

        vote_in = QuestionVoteCreate(user_id=current_user.id, target_id=question_id)
        question = create_question_vote(vote_in=vote_in)

        # user action.
        user_action_in = UserActionVoteQuestionCreate(
            user_id=current_user.id, target_id=question.id
        )
        create_user_action(user_action_in=user_action_in)

        # notification.
        if question.user_id != current_user.id:
            notification_in = NotificationForQuestionVoteCreate(
                user_id=question.user_id,
                notification_target_id=question.id,
                from_user_id=current_user.id,
                to_user_id=question.user_id,
            )
            create_notification(notification_in=notification_in)

    if request.method == HTTPMethod.DELETE:
        if vote is None:
            abort(HTTPStatus.NOT_FOUND)

        question = delete_question_vote(
            question_id=question_id, user_id=current_user.id
        )

        # user action.
        delete_user_action(
            user_id=current_user.id, action_type="vote_question", target_id=question.id
        )

        # notification.
        if question.user_id != current_user.id:
            delete_notification(
                user_id=question.user_id,
                notification_type="vote_question",
                notification_target_id=question.id,
                from_user_id=current_user.id,
                to_user_id=question.user_id,
            )

    return render_template("community/question/vote.html.jinja", question=question)


@bp.route("/posts/<int:post_id>/vote", methods=[HTTPMethod.POST, HTTPMethod.DELETE])
@login_required
def post_vote(post_id: int):
    """
    (POST) Process vote and return fragment.
    (DELETE) Process unvote and return fragment.
    """

    vote = get_post_vote(target_id=post_id, user_id=current_user.id)

    if request.method == HTTPMethod.POST:
        if vote is not None:
            abort(HTTPStatus.CONFLICT)

        vote_in = PostVoteCreate(user_id=current_user.id, target_id=post_id)
        post = create_post_vote(vote_in=vote_in)

        # user action.
        user_action_in = UserActionVotePostCreate(
            user_id=current_user.id, target_id=post.id
        )
        create_user_action(user_action_in=user_action_in)

        # notification.
        if post.user_id != current_user.id:
            notification_in = NotificationForPostVoteCreate(
                user_id=post.user_id,
                notification_target_id=post.id,
                from_user_id=current_user.id,
                to_user_id=post.user_id,
            )
            create_notification(notification_in=notification_in)

    if request.method == HTTPMethod.DELETE:
        if vote is None:
            abort(HTTPStatus.NOT_FOUND)

        post = delete_post_vote(target_id=post_id, user_id=current_user.id)

        # user action.
        delete_user_action(
            user_id=current_user.id, action_type="vote_post", target_id=post_id
        )

        # notification.
        if post.user_id != current_user.id:
            delete_notification(
                user_id=post.user_id,
                notification_type="vote_post",
                notification_target_id=post.id,
                from_user_id=current_user.id,
                to_user_id=post.user_id,
            )

    return render_template("community/post/vote.html.jinja", post=post)


@bp.route("/help/new", methods=[HTTPMethod.GET, HTTPMethod.POST])
@login_required
def question_new():
    """
    (GET) Show new question page.
    (POST) Process new question.
    """

    if request.method == HTTPMethod.POST:
        tags_dict = request.form.get("tags")
        tags_in = []
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

        question = create_question(question_in=question_in, tags_in=tags_in)

        user_action_in = UserActionCreateQuestionCreate(
            user_id=current_user.id, target_id=question.id
        )
        create_user_action(user_action_in=user_action_in)

        return redirect(url_for("pyduck.community.index", category="help"))

    return render_template("community/question/new.html.jinja")


@bp.route("/<category>/new", methods=[HTTPMethod.GET, HTTPMethod.POST])
@login_required
def post_new(category: str):
    """
    (GET) Show new post page.
    (POST) Process new post.
    """

    if request.method == HTTPMethod.POST:
        tags_dict = request.form.get("tags")
        tags_in = []
        if tags_dict:
            tags_in = [tag.get("value") for tag in json.loads(tags_dict)]
            tags_in = get_or_create_post_tags(tags_in=tags_in)

        post_in = None
        try:
            post_in = PostCreate(
                **request.form.to_dict(), user_id=current_user.id, category=category
            )
        except ValidationError as e:
            logger.warn(e.errors)
            return render_template("community/post/new.html.jinja", category=category)

        post = create_post(post_in=post_in, tags_in=tags_in)

        user_action_in = UserActionCreatePostCreate(
            user_id=current_user.id, target_id=post.id
        )
        create_user_action(user_action_in=user_action_in)

        return redirect(url_for("pyduck.community.index", category=category))

    return render_template("community/post/new.html.jinja", category=category)


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
    folder = "csduck/pyduck/community/static/upload/images"

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


@bp.route("/answers", methods=[HTTPMethod.POST, HTTPMethod.PUT, HTTPMethod.DELETE])
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

        # user action.
        user_action_in = UserActionCreateAnswerCreate(
            user_id=current_user.id, target_id=answer.id
        )
        user_action = create_user_action(user_action_in=user_action_in)

        # notification
        if answer.question.user_id != answer.user_id:
            notification_in = NotificationForAnswerCreate(
                user_id=answer.question.user_id,
                notification_target_id=answer.id,
                from_user_id=current_user.id,
                to_user_id=answer.question.user_id,
            )
            create_notification(notification_in=notification_in)

        res = make_response(
            render_template("community/answer/answer.html.jinja", answer=answer)
        )
        res.headers["HX-Trigger-After-Settle"] = "answer-created"

        return res

    # PUT, DELETE pre checking.
    answer_id = request.form.get("answer_id")
    answer = get_answer(answer_id=answer)

    if post_comment is None:
        abort(HTTPStatus.NOT_FOUND)
    if current_user.id != post_comment.user_id:
        abort(HTTPStatus.FORBIDDEN)

    if request.method == HTTPMethod.PUT:
        content = request.form.get("content")
        if content is None:
            abort(HTTPStatus.BAD_REQUEST)

        try:
            answer_in = AnswerUpdate(
                **answer.dict(exclude={"content", "updated_at"}),
                content=content,
                updated_at=datetime.now(timezone.utc),
            )
        except ValidationError as e:
            logger.warn(e.errors())

        answer = update_answer_adding_history(answer_in=answer_in)
        res = make_response(
            render_template("community/answer/answer.html.jinja", answer=answer)
        )

    if request.method == HTTPMethod.DELETE:
        question = delete_answer(answer_id=answer.id)

        # user action.
        delete_user_action(
            user_id=current_user.id, action_type="create_answer", target_id=answer_id
        )

        delete_notification(
            user_id=answer.question.user_id,
            notification_type="create_answer",
            notification_target_id=answer_id,
            from_user_id=current_user.id,
            to_user_id=answer.question.user_id,
        )

    return res


@bp.route("/posts/<int:post_id>/comments", methods=[HTTPMethod.POST])
@bp.route(
    "/posts/<int:post_id>/comments/<int:post_comment_id>",
    methods=[HTTPMethod.PUT, HTTPMethod.DELETE],
)
@login_required
def post_comment(post_id: int, post_comment_id: int | None = None):
    """
    (POST) Create comment to post and return fragment about that comment.
    (PUT) Update comment to post and return fragment about that comment.
    (DELETE) Delete comment.
    """

    if request.method == HTTPMethod.POST:
        post_comment_in = None
        try:
            post_comment_in = PostCommentCreate(
                **request.form.to_dict(), user_id=current_user.id
            )
        except ValidationError as e:
            logger.warn(e.errors())
            abort(HTTPStatus.BAD_REQUEST)

        post_comment = create_post_comment(post_comment_in=post_comment_in)

        # user action.
        user_action_in = UserActionCreatePostCommentCreate(
            user_id=current_user.id, target_id=post_comment.id
        )
        create_user_action(user_action_in=user_action_in)

        # notification.
        if post_comment.post.user_id != post_comment.user_id:
            notification_in = NotificationForPostCommentCreate(
                user_id=post_comment.post.user_id,
                notification_target_id=post_comment.id,
                from_user_id=current_user.id,
                to_user_id=post_comment.post.user_id,
            )
            create_notification(notification_in=notification_in)

        res = make_response(
            render_template(
                "community/post_comment/post_comment.html.jinja",
                post_comment=post_comment,
            )
        )
        res.headers["HX-Trigger-After-Settle"] = "postcomment-created"

        return res

    # PUT, DELETE pre checking.
    post_comment = get_post_comment(post_comment_id=post_comment_id)

    if post_comment is None:
        abort(HTTPStatus.NOT_FOUND)
    if current_user.id != post_comment.user_id:
        abort(HTTPStatus.FORBIDDEN)

    if request.method == HTTPMethod.PUT:
        content = request.form.get("content")

        if content is None:
            abort(HTTPStatus.BAD_REQUEST)

        try:
            post_comment_in = PostCommentUpdate(
                **post_comment.dict(exclude={"content", "updated_at"}),
                content=content,
                updated_at=datetime.now(timezone.utc),
            )
        except ValidationError as e:
            logger.warn(e.errors())

        post_comment = update_post_comment_adding_history(
            post_comment_in=post_comment_in
        )
        res = make_response(
            render_template(
                "community/post_comment/post_comment.html.jinja",
                post_comment=post_comment,
            )
        )

    if request.method == HTTPMethod.DELETE:
        post = delete_post_comment(post_comment_id=post_comment.id)

        # user action.
        delete_user_action(
            user_id=current_user.id,
            action_type="create_post_comment",
            target_id=post_comment_id,
        )

        # notification.
        if post.user_id != current_user.id:
            delete_notification(
                user_id=post_comment.post.user_id,
                notification_type="create_post_comment",
                notification_target_id=post_comment_id,
                from_user_id=current_user.id,
                to_user_id=post_comment.post.user_id,
            )

        res = make_response()
        res.headers["HX-Trigger-After-Settle"] = "postcomment-deleted"

    return res


@bp.route("/answers/<int:answer_id>/vote", methods=[HTTPMethod.POST, HTTPMethod.DELETE])
@login_required
def answer_vote(answer_id: int):
    """
    (POST) Process vote and return fragment.
    (DELETE) Process unvote and return fragment.
    """

    vote = get_answer_vote(answer_id=answer_id, user_id=current_user.id)

    if request.method == HTTPMethod.POST:
        if vote is not None:
            abort(HTTPStatus.CONFLICT)

        vote_in = AnswerVoteCreate(user_id=current_user.id, target_id=answer_id)
        answer = create_answer_vote(vote_in=vote_in)

        # user action.
        user_action_in = UserActionVoteAnswerCreate(
            user_id=current_user.id, target_id=answer.id
        )
        create_user_action(user_action_in=user_action_in)

        # notification.
        if answer.user_id != current_user.id:
            notification_in = NotificationForAnswerVoteCreate(
                user_id=answer.user_id,
                notification_target_id=answer.id,
                from_user_id=current_user.id,
                to_user_id=answer.user_id,
            )
            create_notification(notification_in=notification_in)

    if request.method == HTTPMethod.DELETE:
        if vote is None:
            abort(HTTPStatus.NOT_FOUND)

        answer = delete_answer_vote(answer_id=answer_id, user_id=current_user.id)

        # user action.
        delete_user_action(
            user_id=current_user.id, action_type="vote_answer", target_id=answer.id
        )

        # notification.
        if answer.user_id != current_user.id:
            delete_notification(
                user_id=answer.user_id,
                notification_type="vote_answer",
                notification_target_id=answer.id,
                from_user_id=current_user.id,
                to_user_id=answer.user_id,
            )

    return render_template("community/answer/vote.html.jinja", answer=answer)


@bp.route(
    "/answers/<int:answer_id>/reactions",
    methods=[HTTPMethod.POST],
)
@login_required
def answer_reaction(answer_id: int):
    """
    (POST) Process reaction or unreaction to answer and return fragment.
    """

    action, code = request.form.get("action").split()

    if code not in VALID_REACTION_CODE:
        abort(HTTPStatus.BAD_REQUEST)

    reaction = get_answer_reaction(
        answer_id=answer_id, user_id=current_user.id, code=code
    )

    if action == "react":
        if reaction is not None:
            abort(HTTPStatus.NOT_FOUND)

        reaction_in = AnswerReactionCreate(
            user_id=current_user.id, target_id=answer_id, code=code
        )
        answer = create_answer_reaction(reaction_in=reaction_in)

        # user action.
        user_action_in = UserActionReactionAnswerCreate(
            user_id=current_user.id, target_id=post.id, action_value=code
        )
        user_action = create_user_action(user_action_in=user_action_in)

        # notification.
        if answer.user_id != user_action.user_id:
            notification_in = NotificationForAnswerReactionCreate(
                user_id=answer.user_id,
                notification_value=code,
                notification_target_id=answer.id,
                from_user_id=current_user.id,
                to_user_id=answer.user_id,
            )
            create_notification(notification_in=notification_in)

    if action == "unreact":
        if reaction is None:
            abort(HTTPStatus.CONFLICT)

        answer = delete_answer_reaction(
            answer_id=answer_id, user_id=current_user.id, code=code
        )

        # user action.
        delete_user_action(
            user_id=current_user.id,
            action_type="reaction_answer",
            target_id=answer.id,
            action_value=code,
        )

        # notification.
        if answer.user_id != current_user.id:
            delete_notification(
                user_id=answer.user_id,
                notification_type="reaction_answer",
                notification_target_id=answer.id,
                notification_value=code,
                from_user_id=current_user.id,
                to_user_id=answer.user_id,
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


@bp.route("/posts/<int:post_id>/comments", methods=[HTTPMethod.GET])
def comments_to_post(post_id: int):
    """
    (GET) Show comments to specific post.

    notes:
    - only first level. (not comments to post's comment)
    """

    commons = CommonParameters(**request.args.to_dict())
    pagination = get_all_comments_to_post_by_commons(**commons.dict(), post_id=post_id)

    return render_template(
        "community/post_comment/comments_to_post.html.jinja", pagination=pagination
    )


@bp.route(
    "/posts/<int:post_id>/comments/<int:post_comment_id>/comments",
    methods=[HTTPMethod.POST],
)
@bp.route(
    "/posts/<int:post_id>/comments/<int:post_comment_id>/comments/<int:comment_id>",
    methods=[HTTPMethod.PUT, HTTPMethod.DELETE],
)
@login_required
def comment_to_post_comment(
    post_id: int, post_comment_id: int, comment_id: int | None = None
):
    """
    (POST) Create comment to post comment and relevant fragment
    (PUT) Update comment to post comment and relevant fragment
    (DELETE) Delete comment to post comment and relevant fragment

    notes:
    - depth 2 like 대댓글(comment of comment)
    """

    if request.method == HTTPMethod.POST:
        post_comment_in = None
        try:
            post_comment_in = PostCommentCreate(
                **request.form.to_dict(),
                user_id=current_user.id,
                post_id=post_id,
                parent_id=post_comment_id,
            )
        except ValidationError as e:
            logger.warn(e.errors())
            abort(HTTPStatus.BAD_REQUEST)

        comment = create_comment_to_post_comment(post_comment_in=post_comment_in)

        res = make_response(
            render_template(
                "community/post_comment/comment_to_post_comment.html.jinja",
                comment=comment,
            )
        )
        res.headers["HX-Trigger-After-Settle"] = "comment-to-post-comment-created"

        return res

    # PUT, DELETE pre checking.
    comment = get_comment_to_post_comment(comment_id=comment_id)
    if comment is None:
        abort(HTTPStatus.NOT_FOUND)
    if current_user.id != comment.user_id:
        abort(HTTPStatus.FORBIDDEN)

    if request.method == HTTPMethod.PUT:
        content = request.form.get("content")
        if content is None:
            abort(HTTPStatus.BAD_REQUEST)

        try:
            comment_in = PostCommentUpdate(
                **comment.dict(exclude={"content", "updated_at"}),
                content=content,
                updated_at=datetime.now(timezone.utc),
            )
        except ValidationError as e:
            logger.warn(e.errors())

        comment = update_post_comment_adding_history(post_comment_in=comment_in)
        res = make_response(
            render_template(
                "community/post_comment/comment_to_post_comment.html.jinja",
                comment=comment,
            )
        )

    if request.method == HTTPMethod.DELETE:
        delete_comment_to_post_comment(comment_id=comment.id)
        res = make_response(), HTTPStatus.OK

    return res


@bp.route(
    "/posts/<int:post_id>/comments/<int:post_comment_id>/comments",
    methods=[HTTPMethod.GET],
)
def comments_to_post_comment(post_id: int, post_comment_id: int):
    """
    (GET) Show comments to specific post's comment.
    """

    commons = CommonParameters(**request.args.to_dict())
    pagination = get_all_comments_to_post_comment_by_commons(
        **commons.dict(), post_comment_id=post_comment_id
    )

    return render_template(
        "community/post_comment/comments_to_post_comment.html.jinja",
        pagination=pagination,
    )


@bp.route("answers/<int:answer_id>/comments", methods=[HTTPMethod.POST])
@bp.route(
    "answers/<int:answer_id>/comments/<int:answer_comment_id>",
    methods=[HTTPMethod.PUT, HTTPMethod.DELETE],
)
@login_required
def comment_to_answer(answer_id: int, answer_comment_id: int | None = None):
    """
    (POST) Process comment creation to question's answer.
    (PUT) Process comment modification to qeustion's answer.
    (DELETE) Delete comment to answer.
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

        # user action.
        user_action_in = UserActionCreateAnswerCommentCreate(
            user_id=current_user.id, target_id=comment.id
        )
        create_user_action(user_action_in=user_action_in)

        # notification if needed.
        if comment.answer.user_id != comment.user_id:
            notification_in = NotificationForAnswerCommentCreate(
                user_id=comment.answer.user_id,
                notification_target_id=comment.id,
                from_user_id=current_user.id,
                to_user_id=comment.answer.user_id,
            )
            create_notification(notification_in=notification_in)

        res = make_response(
            render_template(
                "community/answer_comment/answer_comment.html.jinja", comment=comment
            )
        )
        res.headers["HX-Trigger-After-Settle"] = "comment-created"

        return res

    # PUT, DELETE pre checking.
    answer_comment = get_answer_comment(answer_comment_id=answer_comment_id)
    if answer_comment is None:
        abort(HTTPStatus.BAD_REQUEST)
    if answer_comment.user_id != current_user.id:
        abort(HTTPStatus.FORBIDDEN)

    if request.method == HTTPMethod.PUT:
        content = request.form.get("content")

        if content is None:
            abort(HTTPStatus.BAD_REQUEST)

        try:
            answer_comment_in = AnswerCommentUpdate(
                **answer_comment.dict(exclude={"content", "updated_at"}),
                content=content,
                updated_at=datetime.now(timezone.utc),
            )
        except ValidationError as e:
            logger.warn(e.errors())

        answer_comment = update_answer_comment_adding_history(
            answer_comment=answer_comment_in
        )
        res = make_response(
            render_template(
                "community/answer_comment/answer_comment.html.jinja",
                comment=answer_comment,
            )
        )

    # if request.method == HTTPMethod.DELETE:
    #     answer = delete_answer_comment(answer_comment_id=comment.id)

    #     # user action
    #     delete_user_action(
    #         user_id=current_user.id,
    #         action_type="create_answer_comment",
    #         target_id=comment_id,
    #     )

    #     # notification.
    #     delete_notification(
    #         user_id=post_comment.post.user_id,
    #         notification_type="create_post_comment",
    #         notification_target_id=post_comment_id,
    #         from_user_id=current_user.id,
    #         to_user_id=post_comment.post.user_id,
    #     )

    #     res = make_response()
    #     res.headers["HX-Trigger-After-Settle"] = "postcomment-deleted"

    return res


@bp.route(
    "/comments/<int:answer_comment_id>/reactions",
    methods=[HTTPMethod.POST],
)
@login_required
def answer_comment_reaction(answer_comment_id: int):
    """
    (POST) Process reaction or unreaction to comment of answer and return fragment.
    """

    action, code = request.form.get("action").split()

    if code not in VALID_REACTION_CODE:
        abort(HTTPStatus.BAD_REQUEST)

    reaction = get_answer_comment_reaction(
        answer_comment_id=answer_comment_id, user_id=current_user.id, code=code
    )

    if action == "react":
        if reaction is not None:
            abort(HTTPStatus.CONFLICT)

        reaction_in = AnswerCommentReactionCreate(
            user_id=current_user.id, target_id=answer_comment_id, code=code
        )
        answer_comment = create_answer_comment_reaction(reaction_in=reaction_in)

        # user action.
        user_action_in = UserActionReactionAnswerCommentCreate(
            user_id=current_user.id, target_id=answer_comment.id, action_value=code
        )
        user_action = create_user_action(user_action_in=user_action_in)

        # notification.
        if answer_comment.user_id != user_action.user_id:
            notification_in = NotificationForAnswerCommentReactionCreate(
                user_id=answer_comment.user_id,
                notification_value=code,
                notification_target_id=answer_comment.id,
                from_user_id=current_user.id,
                to_user_id=answer_comment.user_id,
            )
            create_notification(notification_in=notification_in)

    if action == "unreact":
        if reaction is None:
            abort(HTTPStatus.NOT_FOUND)

        answer_comment = delete_answer_comment_reaction(
            answer_comment_id=answer_comment_id, user_id=current_user.id, code=code
        )

        # user action.
        delete_user_action(
            user_id=current_user.id,
            action_type="reaction_answer_comment",
            target_id=answer_comment.id,
            action_value=code,
        )

        # notification.
        if answer_comment.user_id != current_user.id:
            delete_notification(
                user_id=answer_comment.user_id,
                notification_type="reaction_answer_comment",
                notification_target_id=answer_comment.id,
                notification_value=code,
                from_user_id=current_user.id,
                to_user_id=answer_comment.user_id,
            )

    return render_template(
        "community/answer_comment/reaction.html.jinja", answer_comment=answer_comment
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


@bp.route(
    "/comments/<int:post_comment_id>/vote", methods=[HTTPMethod.POST, HTTPMethod.DELETE]
)
@login_required
def post_comment_vote(post_comment_id: int):
    """
    (POST) Process vote and return fragment.
    (DELETE) Process unvote and return fragment.
    """

    vote = get_post_comment_vote(
        post_comment_id=post_comment_id, user_id=current_user.id
    )

    if request.method == HTTPMethod.POST:
        if vote is not None:
            abort(HTTPStatus.CONFLICT)

        vote_in = PostCommentVoteCreate(
            user_id=current_user.id,
            target_id=post_comment_id,
        )
        post_comment = create_post_comment_vote(vote_in=vote_in)

        # user action.
        user_action_in = UserActionVotePostCommentCreate(
            user_id=current_user.id, target_id=post_comment.id
        )
        create_user_action(user_action_in=user_action_in)

        # notification.
        if post_comment.user_id != current_user.id:
            notification_in = NotificationForPostCommentVoteCreate(
                user_id=post_comment.user_id,
                notification_target_id=post_comment.id,
                from_user_id=current_user.id,
                to_user_id=post_comment.user_id,
            )
            create_notification(notification_in=notification_in)

    if request.method == HTTPMethod.DELETE:
        if vote is None:
            abort(HTTPStatus.NOT_FOUND)

        post_comment = delete_post_comment_vote(
            post_comment_id=vote.target_id, user_id=vote.user_id
        )

        # user action.
        delete_user_action(
            user_id=current_user.id,
            action_type="vote_post_comment",
            target_id=delete_user_action.id,
        )

        # notification.
        if post_comment.user_id != current_user.id:
            delete_notification(
                user_id=post_comment.user_id,
                notification_type="vote_post_comment",
                notification_target_id=post_comment.id,
                from_user_id=current_user.id,
                to_user_id=post_comment.user_id,
            )

    return render_template(
        "community/post_comment/vote.html.jinja", post_comment=post_comment
    )
