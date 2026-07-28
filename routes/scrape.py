"""Manual scrape trigger endpoints."""

from __future__ import annotations

import logging

from flask import Blueprint, jsonify, request

from services.scraper_service import scrape_all_sources
from utils.errors import APIError

logger = logging.getLogger(__name__)

scrape_bp = Blueprint("scrape", __name__)


def _parse_force_full() -> bool:
    raw = request.args.get("force_full", "false").strip().lower()
    if raw in ("true", "1", "yes"):
        return True
    if raw in ("false", "0", "no", ""):
        return False
    raise APIError(
        f"Invalid 'force_full': expected true/false, got '{raw}'.",
        status_code=400,
    )


@scrape_bp.get("/api/scrape")
def manual_scrape():
    """Manually run all enabled scrapers. Errors from individual sources are
    captured inside the scrape result (result.errors) rather than failing the
    whole request; only unexpected orchestration failures return a 500."""
    force_full = _parse_force_full()
    try:
        result = scrape_all_sources(force_full=force_full)
    except Exception as exc:  # pragma: no cover - orchestration-level safety net
        logger.exception("Manual scrape failed unexpectedly: %s", exc)
        raise APIError("Scrape run failed unexpectedly. Check server logs.", status_code=500)
    return jsonify({"status": "ok", "action": "manual_scrape", "result": result}), 200


@scrape_bp.get("/api/refresh")
def force_refresh():
    """Force an immediate incremental refresh (never re-scrapes known URLs)."""
    try:
        result = scrape_all_sources(force_full=False)
    except Exception as exc:  # pragma: no cover
        logger.exception("Refresh failed unexpectedly: %s", exc)
        raise APIError("Refresh run failed unexpectedly. Check server logs.", status_code=500)
    return jsonify({"status": "ok", "action": "refresh", "result": result}), 200
