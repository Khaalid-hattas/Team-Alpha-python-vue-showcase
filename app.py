"""Flask API for news scraping, storage, and scheduler control."""

from __future__ import annotations

import logging
import os
from html import escape
from string import Template

from flask import Flask, jsonify, request

from services.scraper_service import get_scheduler_status, scrape_all_sources, start_scheduler
from services.storage import get_articles, init_storage


ROOT_PREVIEW_LIMIT = 12


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
    articles = get_articles(limit=ROOT_PREVIEW_LIMIT)

    article_cards: list[str] = []
    for article in articles:
        title = escape(article.get("title") or "Untitled article")
        source = escape(article.get("source") or "Unknown source")
        published = escape(article.get("published") or article.get("scraped_at") or "")
        url = escape(article.get("url") or "#")
        summary = escape(article.get("summary") or article.get("description") or "No summary available.")

        article_cards.append(
            f"""
            <article class="card">
                <p class="eyebrow">{source}</p>
                <h2><a href="{url}" target="_blank" rel="noreferrer">{title}</a></h2>
                <p class="meta">{published}</p>
                <p>{summary}</p>
            </article>
            """
        )

    article_list = "\n".join(article_cards) if article_cards else "<p class=\"empty\">No articles are stored yet. Run <a href=\"/api/scrape\">/api/scrape</a> to populate the database.</p>"

    page = Template(
        """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Team Alpha News Scraper API</title>
    <style>
        :root {
            color-scheme: light;
            --bg: #eef4ff;
            --panel: #ffffff;
            --text: #102033;
            --muted: #536173;
            --line: #d7e1f1;
            --accent: #0057b8;
            --accent-soft: #e8f1ff;
        }
        body {
            margin: 0;
            font-family: "Segoe UI", Tahoma, sans-serif;
            background:
                radial-gradient(circle at top left, rgba(0, 87, 184, 0.14), transparent 28%),
                linear-gradient(135deg, var(--bg), #f8fbff 55%, #edf5ff);
            color: var(--text);
        }
        .wrap {
            max-width: 1040px;
            margin: 5vh auto;
            padding: 24px;
        }
        .hero, .panel {
            background: var(--panel);
            border: 1px solid var(--line);
            border-radius: 18px;
            box-shadow: 0 16px 40px rgba(16, 32, 51, 0.08);
        }
        .hero {
            padding: 28px;
            margin-bottom: 18px;
        }
        h1 {
            margin: 0 0 8px;
            font-size: clamp(2rem, 3vw, 3rem);
            line-height: 1.05;
        }
        p {
            margin: 0 0 16px;
            color: var(--muted);
            .hero-row {
        }}
        .hero-row {{
            display: flex;
            gap: 12px;
            }
            .pill, .button {
        }
        .pill, .button {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            border-radius: 999px;
            padding: 10px 14px;
            }
            .pill {
        }}
        .pill {{
            }
            .button {
        }}
        .button {{
            }
            .panel {
        }}
            }
            .panel h2 {
        }}
        .panel h2 {{
            }
            .grid {
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            }
            .card {
        }}
        .card {{
            border: 1px solid var(--line);
            border-radius: 14px;
            }
            .card h2 {
        }}
        .card h2 {{
            margin: 0 0 8px;
            font-size: 1.05rem;
            .card a {
        }
        .card a {{
            }
            .card a:hover {
        }}
            }
            .eyebrow {
        }}
        .eyebrow {{
            margin: 0 0 10px;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-size: 0.74rem;
            }
            .meta {
        }}
        .meta {{
            font-size: 0.85rem;
            }
            .links {
        }
        .links {{
            display: flex;
            flex-wrap: wrap;
            }
            .empty {
        }
        .empty {{
            margin: 0;
            padding: 18px;
            border: 1px dashed var(--line);
            }
            .empty a {
        }
        .empty a {{
            }
            font-weight: 700;
        }
    </style>
</head>
<body>
    <main class="wrap">
        <section class="hero">
            <p class="eyebrow">Local host connected</p>
            <h1>Team Alpha News Scraper API</h1>
            <p>Live articles are loaded from the SQLite data store behind this host page.</p>
            <div class="hero-row">
                <a class="button" href="/api/articles">View JSON feed</a>
                <a class="pill" href="/api/scrape">Run full scrape</a>
                <a class="pill" href="/api/status">Check status</a>
            </div>
            <div class="links">
                <a class="pill" href="/api/refresh">Refresh now</a>
            </div>
        </section>
        <section class="panel">
            <h2>Latest stored articles</h2>
            <p>Showing the newest $ARTICLE_COUNT records from the connected data store.</p>
            <div class="grid">
                $ARTICLE_LIST
            </div>
        </section>
    </main>
</body>
</html>
        """
    ).substitute(
        ARTICLE_COUNT=len(articles),
        ARTICLE_LIST=article_list,
    )

    return (
            page,
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
