"""Storage and normalization layer for scraped news items."""

from __future__ import annotations

import json
import logging
import sqlite3
from pathlib import Path
from typing import Any, Optional

from utils.scraper_helpers import normalize_text, parse_datetime, utc_now_iso

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DB_PATH = DATA_DIR / "articles.db"


def _get_connection() -> sqlite3.Connection:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_storage() -> None:
    """Initialize sqlite storage schema."""
    with _get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT,
                title TEXT,
                summary TEXT,
                description TEXT,
                author TEXT,
                published TEXT,
                image TEXT,
                category TEXT,
                tags TEXT,
                content TEXT,
                url TEXT NOT NULL UNIQUE,
                scraped_at TEXT
            )
            """
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_articles_source ON articles(source)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_articles_published ON articles(published)")
        conn.commit()


def normalize_item(item: dict[str, Any]) -> dict[str, Any]:
    """Normalize scraped article shape before persistence."""
    tags = item.get("tags")
    if not isinstance(tags, list):
        tags = []

    url = normalize_text(item.get("url"))

    return {
        "source": normalize_text(item.get("source")),
        "title": normalize_text(item.get("title")),
        "summary": normalize_text(item.get("summary")),
        "description": normalize_text(item.get("description")),
        "author": normalize_text(item.get("author")),
        "published": parse_datetime(item.get("published")),
        "image": normalize_text(item.get("image")),
        "category": normalize_text(item.get("category")),
        "tags": [normalize_text(tag) for tag in tags if normalize_text(tag)],
        "content": normalize_text(item.get("content")),
        "url": url,
        "scraped_at": parse_datetime(item.get("scraped_at")) or utc_now_iso(),
    }


def save_items(items: list[dict[str, Any]]) -> dict[str, int]:
    """Persist normalized articles, skipping duplicate URLs."""
    saved = 0
    duplicates = 0

    with _get_connection() as conn:
        for item in items:
            if not item.get("url"):
                continue

            cursor = conn.execute(
                """
                INSERT OR IGNORE INTO articles (
                    source, title, summary, description, author, published,
                    image, category, tags, content, url, scraped_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    item.get("source"),
                    item.get("title"),
                    item.get("summary"),
                    item.get("description"),
                    item.get("author"),
                    item.get("published"),
                    item.get("image"),
                    item.get("category"),
                    json.dumps(item.get("tags") or []),
                    item.get("content"),
                    item.get("url"),
                    item.get("scraped_at"),
                ),
            )
            if cursor.rowcount == 0:
                duplicates += 1
            else:
                saved += 1

        conn.commit()

    return {"saved": saved, "duplicates": duplicates}


def get_all_urls() -> set[str]:
    """Return all known article URLs for duplicate avoidance."""
    with _get_connection() as conn:
        rows = conn.execute("SELECT url FROM articles WHERE url IS NOT NULL").fetchall()
    return {row["url"] for row in rows if row["url"]}


def get_articles(limit: int = 500, source: Optional[str] = None) -> list[dict[str, Any]]:
    """Read stored articles sorted by publish/scrape date."""
    sql = """
        SELECT source, title, summary, description, author, published,
               image, category, tags, content, url, scraped_at
        FROM articles
    """
    params: list[Any] = []
    if source:
        sql += " WHERE source = ?"
        params.append(source)
    sql += " ORDER BY COALESCE(published, scraped_at) DESC LIMIT ?"
    params.append(limit)

    with _get_connection() as conn:
        rows = conn.execute(sql, tuple(params)).fetchall()

    articles: list[dict[str, Any]] = []
    for row in rows:
        tags_value = row["tags"]
        try:
            tags = json.loads(tags_value) if tags_value else []
        except json.JSONDecodeError:
            tags = []

        articles.append(
            {
                "source": row["source"],
                "title": row["title"],
                "summary": row["summary"],
                "description": row["description"],
                "author": row["author"],
                "published": row["published"],
                "image": row["image"],
                "category": row["category"],
                "tags": tags,
                "content": row["content"],
                "url": row["url"],
                "scraped_at": row["scraped_at"],
            }
        )
    return articles


def get_article_count() -> int:
    """Return total number of stored articles."""
    with _get_connection() as conn:
        row = conn.execute("SELECT COUNT(1) AS count FROM articles").fetchone()
    return int(row["count"]) if row else 0
