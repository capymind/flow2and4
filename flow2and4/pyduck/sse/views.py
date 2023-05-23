"""
This is the module for defining SSEs(Server-Sent Events).

[stolen and modified from]
- https://github.com/singingwolfboy/flask-sse/blob/main/flask_sse.py
- https://github.com/sysid/sse-starlette/blob/master/sse_starlette/sse.py
"""

from flask import Blueprint, current_app, stream_with_context, make_response, Response
from redis import Redis
import time
import json


class EventStream:
    """Represent text/event-stream."""

    def __init__(
        self,
        data: str | None = None,
        event: str | None = None,
        id: str | None = None,
        retry: int | None = 15000,
        comment: str | None = None,
    ):
        """Initialize EventStream."""

        self.data = data
        self.event = event
        self.id = id
        self.retry = retry
        self.comment = comment

    def __str__(self):
        """Process event stream instance into string following spec.

        https://html.spec.whatwg.org/multipage/server-sent-events.html#parsing-an-event-stream
        """

        lines = []
        if self.event is not None:
            lines.append(f"event:{self.event}")
        if self.data is not None:
            lines.extend([f"data:{value}" for value in self.data.splitlines()])
        if self.id is not None:
            lines.append(f"id:{self.id}")
        if self.retry is not None:
            lines.append(f"retry:{self.retry}")
        if self.comment is not None:
            lines.append(f":{self.comment}")

        if len(lines) == 0:
            raise ValueError("at least one field have to have field value.")

        return "\n".join(lines) + "\n\n"

    def to_dict(self):
        """Convert EventStream instance into a dict for storing in Redis."""

        d = {}

        if self.event is not None:
            d.update({"event": self.event})
        if self.data is not None:
            d.update({"data": self.data})
        if self.id is not None:
            d.update({"id": self.id})
        if self.retry is not None:
            d.update({"retry": self.retry})
        if self.comment is not None:
            d.update({"comment": self.comment})

        if len(d.keys()) == 0:
            raise ValueError("at least one filed have to have field value.")

        return d


class BlueprintWithSSE(Blueprint):
    """Represent Blueprint with SSE functionality added by redis pub/sub."""

    @property
    def redis(self):
        """Represent a redis connection."""

        url = current_app.config.get("REDIS_CONNECTION_URL_FOR_SERVER_SENT_EVENTS")
        if url is None:
            raise KeyError("Redis url is needed for enabling SSE functionality.")

        return Redis.from_url(url=url)

    def publish(self, message: EventStream, channel: str = "sse"):
        """Publish event stream to redis pub/sub."""

        if not isinstance(message, EventStream):
            raise TypeError("message to be sent must follow text/event-stream for SSE.")

        return self.redis.publish(
            channel=channel, message=json.dumps(message.to_dict())
        )


bp = BlueprintWithSSE("sse", __name__, url_prefix="/stream")


@bp.route("/users/<int:user_id>")
def stream_to_user(user_id: int):
    """Stream server-sent events to specific user."""

    @stream_with_context
    def generate():
        """get message if exists and yield that."""

        pubsub = bp.redis.pubsub(ignore_subscribe_messages=True)
        pubsub.subscribe(user_id)

        while True:
            message = pubsub.get_message()
            if message is None:
                yield str(EventStream(comment="ping"))
            else:
                yield str(EventStream(**json.loads(message["data"])))
            time.sleep(2.5)  # be nice to the system :)

    res = Response(generate(), mimetype="text/event-stream")
    res.headers["X-Accel-Buffering"] = "no"

    return res
