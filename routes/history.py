"""Scrape run history endpoint."""

from __future__ import annotations

from flask import Blueprint, jsonify, request

from services.storage import get_run_history
from utils.validation import parse_int

history_bp = Blueprint("history", __name__)


@history_bp.get("/api/history")
def api_history():
    """List historical scraping runs and execution timestamps."""
    limit = parse_int(request.args.get("limit"), default=50, minimum=1, maximum=200, field_name="limit")
    offset = parse_int(request.args.get("offset"), default=0, minimum=0, field_name="offset")

    runs, total = get_run_history(limit=limit, offset=offset)

    return jsonify(
        {
            "status": "ok",
            "count": len(runs),
            "total": total,
            "limit": limit,
            "offset": offset,
            "runs": runs,
        }
    ), 200
