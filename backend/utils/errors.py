"""Centralized API error handling.

Every error response from this API (validation failures, not-found, or
unexpected server errors) is returned as JSON with the shape:

    {"status": "error", "message": "...", "details": {...optional...}}

so the Vue frontend can rely on a single, consistent error contract instead
of sometimes getting Flask's default HTML error pages.
"""

from __future__ import annotations

import logging

from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

logger = logging.getLogger(__name__)


class APIError(Exception):
    """Raised by route handlers for expected, client-facing error conditions.

    Use this instead of letting validation problems raise bare ValueErrors,
    KeyErrors, etc. so the caller always gets a clean JSON response and the
    correct HTTP status code (default 400).
    """

    def __init__(self, message: str, status_code: int = 400, details: dict | None = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details or {}

    def to_dict(self) -> dict:
        payload = {"status": "error", "message": self.message}
        if self.details:
            payload["details"] = self.details
        return payload


def register_error_handlers(app: Flask) -> None:
    """Attach JSON error handlers to the Flask app."""

    @app.errorhandler(APIError)
    def handle_api_error(error: APIError):
        return jsonify(error.to_dict()), error.status_code

    @app.errorhandler(404)
    def handle_not_found(error):
        return jsonify({"status": "error", "message": "Resource not found."}), 404

    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        return jsonify({"status": "error", "message": "Method not allowed on this endpoint."}), 405

    @app.errorhandler(HTTPException)
    def handle_http_exception(error: HTTPException):
        # Catches any other Werkzeug HTTP error (400, 413, etc.) with a JSON body.
        return jsonify({"status": "error", "message": error.description or error.name}), error.code or 500

    @app.errorhandler(Exception)
    def handle_unexpected_error(error: Exception):
        # Last-resort safety net: never let an unhandled exception fall through
        # to a generic HTML 500 page. Log the full traceback, but don't leak
        # internal details to the client.
        logger.exception("Unhandled exception in request: %s", error)
        return (
            jsonify({"status": "error", "message": "An unexpected error occurred. Please try again."}),
            500,
        )
