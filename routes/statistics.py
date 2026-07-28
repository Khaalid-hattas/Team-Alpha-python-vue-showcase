"""Summary statistics endpoint."""

from __future__ import annotations

from flask import Blueprint, jsonify

from services.storage import (
    get_article_count,
    get_last_run,
    get_source_breakdown,
    get_websites,
)

statistics_bp = Blueprint("statistics", __name__)


@statistics_bp.get("/api/statistics")
def api_statistics():
    """Return summary stats: total items, per-source breakdown, target count,
    and a success rate derived from the most recent scrape run."""
    total_items = get_article_count()
    websites = get_websites()
    last_run = get_last_run()

    if last_run and last_run.get("found"):
        success_rate = round(100 * last_run["saved"] / last_run["found"], 1)
    elif last_run:
        # Nothing new found is still a successful run (no duplicates/errors).
        success_rate = 100.0 if not last_run.get("errors") else 0.0
    else:
        success_rate = None

    return jsonify(
        {
            "status": "ok",
            "total_items": total_items,
            "total_websites": len(websites),
            "enabled_websites": sum(1 for site in websites if site["enabled"]),
            "sources": get_source_breakdown(),
            "success_rate": success_rate,
            "last_run": last_run,
        }
    ), 200
