"""Health check and scheduler status endpoints."""

from __future__ import annotations

import sqlite3

from flask import Blueprint, jsonify

from services.scraper_service import get_scheduler_status
from services.storage import DB_PATH

health_bp = Blueprint("health", __name__)


def _database_reachable() -> bool:
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("SELECT 1")
        conn.close()
        return True
    except sqlite3.Error:
        return False


@health_bp.get("/api/health")
def api_health():
    """Liveness/readiness probe: verifies the DB is reachable.

    Returns 200 when healthy, 503 when the storage layer can't be reached.
    """
    db_ok = _database_reachable()
    scheduler_status = get_scheduler_status()

    payload = {
        "status": "ok" if db_ok else "error",
        "checks": {
            "database": "ok" if db_ok else "unreachable",
            "scheduler": "running" if scheduler_status["running"] else "stopped",
        },
    }
    return jsonify(payload), 200 if db_ok else 503


@health_bp.get("/api/status")
def api_status():
    """Return scheduler and storage status. Kept for backwards compatibility
    with clients built against the original /api/status endpoint."""
    status = get_scheduler_status()
    return jsonify({"status": "ok", "scheduler": status}), 200
