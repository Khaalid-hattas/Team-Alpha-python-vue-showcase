"""Simple HTML landing page for browser sanity checks."""

from __future__ import annotations

from html import escape
from string import Template

from flask import Blueprint

from services.storage import get_articles

pages_bp = Blueprint("pages", __name__)

ROOT_PREVIEW_LIMIT = 12

PAGE_TEMPLATE = Template(
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
        .wrap { max-width: 1040px; margin: 5vh auto; padding: 24px; }
        .hero, .panel {
            background: var(--panel);
            border: 1px solid var(--line);
            border-radius: 18px;
            box-shadow: 0 16px 40px rgba(16, 32, 51, 0.08);
        }
        .hero { padding: 28px; margin-bottom: 18px; }
        h1 { margin: 0 0 8px; font-size: clamp(2rem, 3vw, 3rem); line-height: 1.05; }
        p { margin: 0 0 16px; color: var(--muted); }
        .hero-row { display: flex; gap: 12px; flex-wrap: wrap; }
        .pill, .button {
            display: inline-flex; align-items: center; gap: 8px;
            border-radius: 999px; padding: 10px 14px;
        }
        .panel h2 { margin: 0 0 8px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; }
        .card { border: 1px solid var(--line); border-radius: 14px; padding: 16px; }
        .card h2 { margin: 0 0 8px; font-size: 1.05rem; }
        .eyebrow { margin: 0 0 10px; text-transform: uppercase; letter-spacing: 0.08em; font-size: 0.74rem; }
        .meta { font-size: 0.85rem; }
        .links { display: flex; flex-wrap: wrap; }
        .empty { margin: 0; padding: 18px; border: 1px dashed var(--line); }
        .empty a { font-weight: 700; }
    </style>
</head>
<body>
    <main class="wrap">
        <section class="hero">
            <p class="eyebrow">Local host connected</p>
            <h1>Team Alpha News Scraper API</h1>
            <p>Live articles are loaded from the SQLite data store behind this host page.</p>
            <div class="hero-row">
                <a class="button" href="/api/items">View JSON feed</a>
                <a class="pill" href="/api/scrape">Run full scrape</a>
                <a class="pill" href="/api/health">Health check</a>
                <a class="pill" href="/api/statistics">Statistics</a>
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
)


@pages_bp.get("/")
def root():
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

    article_list = "\n".join(article_cards) if article_cards else (
        '<p class="empty">No articles are stored yet. Run '
        '<a href="/api/scrape">/api/scrape</a> to populate the database.</p>'
    )

    page = PAGE_TEMPLATE.substitute(ARTICLE_COUNT=len(articles), ARTICLE_LIST=article_list)
    return page, 200, {"Content-Type": "text/html; charset=utf-8"}
