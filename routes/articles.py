"""Article listing and search endpoints."""

from __future__ import annotations

from flask import Blueprint, jsonify, request

from services.storage import get_article_count, get_articles, search_articles
from utils.validation import parse_int, require_str

articles_bp = Blueprint("articles", __name__)

MAX_LIMIT = 500


def _list_articles():
    limit = parse_int(request.args.get("limit"), default=200, minimum=1, maximum=MAX_LIMIT, field_name="limit")
    offset = parse_int(request.args.get("offset"), default=0, minimum=0, field_name="offset")
    source = request.args.get("source") or None

    items = get_articles(limit=limit, offset=offset, source=source)
    total = get_article_count(source=source)

    return jsonify(
        {
            "status": "ok",
            "count": len(items),
            "total": total,
            "limit": limit,
            "offset": offset,
            "items": items,
        }
    ), 200


@articles_bp.get("/api/items")
def api_items():
    """Retrieve stored scraped items with pagination support (brief-spec name)."""
    return _list_articles()


@articles_bp.get("/api/articles")
def api_articles():
    """Alias of /api/items, kept for backward compatibility with the existing frontend."""
    return _list_articles()


@articles_bp.get("/api/search")
def api_search():
    """Filter scraped items matching a free-text search query."""
    query = require_str(request.args.get("q"), field_name="q")
    limit = parse_int(request.args.get("limit"), default=50, minimum=1, maximum=MAX_LIMIT, field_name="limit")
    offset = parse_int(request.args.get("offset"), default=0, minimum=0, field_name="offset")
    source = request.args.get("source") or None

    results, total = search_articles(query=query, limit=limit, offset=offset, source=source)

    return jsonify(
        {
            "status": "ok",
            "query": query,
            "count": len(results),
            "total": total,
            "limit": limit,
            "offset": offset,
            "items": results,
        }
    ), 200
