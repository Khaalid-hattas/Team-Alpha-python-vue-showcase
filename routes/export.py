"""Data export endpoint -- CSV and JSON downloads of scraped articles."""

from __future__ import annotations

import csv
import io
import json

from flask import Blueprint, Response, request

from services.storage import get_articles
from utils.errors import APIError
from utils.validation import parse_int

export_bp = Blueprint("export", __name__)

CSV_FIELDS = [
    "source", "title", "summary", "description", "author",
    "published", "image", "category", "tags", "url", "scraped_at",
]


@export_bp.get("/api/export")
def api_export():
    """Export stored articles as a CSV or JSON file download.

    Query params:
      format=csv|json (default json)
      source=<name>   (optional filter)
      limit=<n>        (default 1000, max 5000)
    """
    fmt = (request.args.get("format") or "json").strip().lower()
    if fmt not in ("csv", "json"):
        raise APIError(f"Invalid 'format': expected 'csv' or 'json', got '{fmt}'.", status_code=400)

    limit = parse_int(request.args.get("limit"), default=1000, minimum=1, maximum=5000, field_name="limit")
    source = request.args.get("source") or None

    items = get_articles(limit=limit, offset=0, source=source)

    if fmt == "json":
        body = json.dumps({"count": len(items), "items": items}, indent=2)
        return Response(
            body,
            mimetype="application/json",
            headers={"Content-Disposition": "attachment; filename=articles_export.json"},
        )

    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=CSV_FIELDS, extrasaction="ignore")
    writer.writeheader()
    for item in items:
        row = dict(item)
        row["tags"] = ", ".join(row.get("tags") or [])
        writer.writerow(row)

    return Response(
        buffer.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=articles_export.csv"},
    )
