import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


DB_PATH = Path(__file__).resolve().parents[1] / "data" / "scraped_items.db"


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS scraped_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT NOT NULL,
                topic TEXT NOT NULL,
                title TEXT NOT NULL,
                summary TEXT,
                description TEXT,
                author TEXT,
                image TEXT,
                tags TEXT,
                url TEXT NOT NULL UNIQUE,
                scraped_at TEXT NOT NULL
            )
            """
        )
        connection.execute(
            "CREATE INDEX IF NOT EXISTS idx_scraped_items_topic ON scraped_items(topic)"
        )
        connection.execute(
            "CREATE INDEX IF NOT EXISTS idx_scraped_items_source ON scraped_items(source)"
        )


def save_items(items):
    if not items:
        return []

    timestamp = datetime.now(timezone.utc).isoformat()

    with get_connection() as connection:
        for item in items:
            connection.execute(
                """
                INSERT INTO scraped_items (
                    source,
                    topic,
                    title,
                    summary,
                    description,
                    author,
                    image,
                    tags,
                    url,
                    scraped_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(url) DO UPDATE SET
                    source=excluded.source,
                    topic=excluded.topic,
                    title=excluded.title,
                    summary=excluded.summary,
                    description=excluded.description,
                    author=excluded.author,
                    image=excluded.image,
                    tags=excluded.tags,
                    scraped_at=excluded.scraped_at
                """,
                (
                    item.get("source", ""),
                    item.get("topic", ""),
                    item.get("title", ""),
                    item.get("summary", ""),
                    item.get("description", ""),
                    item.get("author", ""),
                    item.get("image", ""),
                    json.dumps(item.get("tags") or []),
                    item.get("url", ""),
                    timestamp,
                ),
            )

    return items


def get_items(topic=None, source=None, limit=50):
    query = """
        SELECT source, topic, title, summary, description, author, image, tags, url, scraped_at
        FROM scraped_items
    """
    clauses = []
    params = []

    if topic:
        clauses.append("topic = ?")
        params.append(topic)

    if source:
        clauses.append("source = ?")
        params.append(source)

    if clauses:
        query += " WHERE " + " AND ".join(clauses)

    query += " ORDER BY datetime(scraped_at) DESC LIMIT ?"
    params.append(max(1, min(limit, 200)))

    with get_connection() as connection:
        rows = connection.execute(query, params).fetchall()

    items = []
    for row in rows:
        items.append(
            {
                "source": row["source"],
                "topic": row["topic"],
                "title": row["title"],
                "summary": row["summary"] or "",
                "description": row["description"] or "",
                "author": row["author"] or "",
                "image": row["image"] or "",
                "tags": json.loads(row["tags"]) if row["tags"] else [],
                "url": row["url"],
                "scraped_at": row["scraped_at"],
            }
        )

    return items
