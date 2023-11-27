from flask import request
import structlog
import uuid

from functools import wraps


def extend_logging_context(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            request_id=request.headers.get("X-Request-ID", str(uuid.uuid4()))
        )
        return f(*args, **kwargs)
    return decorator
