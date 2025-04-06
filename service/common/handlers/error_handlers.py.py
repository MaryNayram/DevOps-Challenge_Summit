"""
Custom Error Handlers for the Fitness Booking API
"""

from flask import jsonify
from api import app
from .http_status.py import HTTPStatus


# ===========================
# Custom Error Handlers
# ===========================

@app.errorhandler(HTTPStatus.BAD_REQUEST)
def handle_bad_request(error):
    """400 — Request could not be understood by the server."""
    app.logger.warning(f"Bad Request: {error}")
    return jsonify(
        status=HTTPStatus.BAD_REQUEST,
        error="Invalid request format or parameters.",
        message=str(error)
    ), HTTPStatus.BAD_REQUEST


@app.errorhandler(HTTPStatus.NOT_FOUND)
def handle_not_found(error):
    """404 — Resource not found."""
    app.logger.warning(f"Not Found: {error}")
    return jsonify(
        status=HTTPStatus.NOT_FOUND,
        error="The requested resource does not exist.",
        message=str(error)
    ), HTTPStatus.NOT_FOUND


@app.errorhandler(HTTPStatus.METHOD_NOT_ALLOWED)
def handle_method_not_allowed(error):
    """405 — Method not allowed on this endpoint."""
    app.logger.warning(f"Method Not Allowed: {error}")
    return jsonify(
        status=HTTPStatus.METHOD_NOT_ALLOWED,
        error="This method is not supported on this route.",
        message=str(error)
    ), HTTPStatus.METHOD_NOT_ALLOWED


@app.errorhandler(HTTPStatus.CONFLICT)
def handle_conflict(error):
    """409 — Conflict with current state of resource."""
    app.logger.warning(f"Conflict: {error}")
    return jsonify(
        status=HTTPStatus.CONFLICT,
        error="Conflict: Resource already exists or is in use.",
        message=str(error)
    ), HTTPStatus.CONFLICT


@app.errorhandler(HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
def handle_unsupported_media(error):
    """415 — Unsupported media type submitted."""
    app.logger.warning(f"Unsupported Media: {error}")
    return jsonify(
        status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
        error="Unsupported media type — check content headers.",
        message=str(error)
    ), HTTPStatus.UNSUPPORTED_MEDIA_TYPE


@app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
def handle_internal_error(error):
    """500 — Unhandled exception or server crash."""
    app.logger.error(f"Internal Server Error: {error}")
    return jsonify(
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
        error="Oops! Something went wrong on our end.",
        message=str(error)
    ), HTTPStatus.INTERNAL_SERVER_ERROR
