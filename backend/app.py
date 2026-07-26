"""Flask API for news scraping, storage, and scheduler control."""

from __future__ import annotations

import logging
import os

from flask import Flask, jsonify, request

from services.scraper_service import get_scheduler_status, scrape_all_sources, start_scheduler
from services.storage import get_articles, init_storage


def configure_logging() -> None:
    """Set baseline logging format and level."""
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO"),
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )


configure_logging()
logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.get("/")
def root() -> tuple:
        """Simple HTML landing page for browser checks."""
        return (
                """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Team Alpha News Scraper API</title>
    <style>
        body {
            margin: 0;
            font-family: "Segoe UI", Tahoma, sans-serif;
            background: linear-gradient(135deg, #f7fafc, #e7f1ff);
            color: #123;
        }
        .wrap {
            max-width: 760px;
            margin: 6vh auto;
            background: #ffffff;
            border: 1px solid #dfe8f5;
            border-radius: 14px;
            padding: 24px;
            box-shadow: 0 10px 24px rgba(18, 44, 82, 0.08);
        }
        h1 {
            margin: 0 0 8px;
            font-size: 1.55rem;
        }
        p {
            margin: 0 0 16px;
            color: #445;
        }
        ul {
            margin: 0;
            padding-left: 20px;
        }
        li {
            margin: 8px 0;
        }
        a {
            color: #0057b8;
            text-decoration: none;
            font-weight: 600;
        }
        a:hover {
            text-decoration: underline;
        }
        .muted {
            margin-top: 18px;
            font-size: 0.92rem;
            color: #667;
        }
    </style>
</head>
<body>
    <main class="wrap">
        <h1>Team Alpha News Scraper API</h1>
        <p>Service is running. Use the endpoints below.</p>
        <ul>
            <li><a href="/api/scrape">/api/scrape</a></li>
            <li><a href="/api/refresh">/api/refresh</a></li>
            <li><a href="/api/articles">/api/articles</a></li>
            <li><a href="/api/status">/api/status</a></li>
        </ul>
        <p class="muted">Scheduler and scraper logs are available in the backend runtime terminal.</p>
    </main>
</body>
</html>
                """,
                200,
                {"Content-Type": "text/html; charset=utf-8"},
        )


@app.get("/api/scrape")
def manual_scrape() -> tuple:
    """Manually run all scrapers."""
    force_full = request.args.get("force_full", "false").lower() == "true"
    result = scrape_all_sources(force_full=force_full)
    return jsonify({"status": "ok", "action": "manual_scrape", "result": result}), 200


@app.get("/api/refresh")
def force_refresh() -> tuple:
    """Force an immediate incremental refresh."""
    result = scrape_all_sources(force_full=False)
    return jsonify({"status": "ok", "action": "refresh", "result": result}), 200


@app.get("/api/articles")
def api_articles() -> tuple:
    """Return stored article list."""
    limit = int(request.args.get("limit", "200"))
    source = request.args.get("source")
    items = get_articles(limit=limit, source=source)
    return jsonify({"status": "ok", "count": len(items), "items": items}), 200


@app.get("/api/status")
def api_status() -> tuple:
    """Return scheduler and storage status."""
    status = get_scheduler_status()
    return jsonify({"status": "ok", "scheduler": status}), 200


def bootstrap() -> None:
    """Initialize storage and start scheduler."""
    init_storage()
    start_scheduler()
    logger.info("Application bootstrap complete")


bootstrap()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False)
