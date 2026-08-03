"""News24 scraper implementation."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Optional, Set

from bs4 import BeautifulSoup

from utils.scraper_helpers import (
    build_session,
    collect_metadata,
    extract_article_body,
    extract_links_from_listing,
    fetch_url,
    normalize_text,
)

SOURCE_NAME = "News24"
BASE_URL = "https://www.news24.com"
TOPIC_URLS = {
    "latest": "https://www.news24.com/news24",
    "business": "https://www.news24.com/fin24",
    "sport": "https://www.news24.com/sport",
    "investigations": "https://www.news24.com/news24/investigations",
}

logger = logging.getLogger(__name__)


def scrape_article(url: str, topic: Optional[str] = None) -> Optional[dict]:
    """Scrape a single News24 article."""
    session = build_session()
    return _scrape_article_with_session(session=session, url=url, topic=topic)


def _scrape_article_with_session(session, url: str, topic: Optional[str] = None) -> Optional[dict]:
    html = fetch_url(session=session, url=url, logger=logger)
    if not html:
        return None

    soup = BeautifulSoup(html, "html.parser")
    metadata = collect_metadata(soup=soup, article_url=url)
    content = extract_article_body(soup)

    if not metadata.get("title") and not content:
        return None

    return {
        "source": SOURCE_NAME,
        "title": normalize_text(metadata.get("title")),
        "summary": normalize_text(metadata.get("summary")),
        "description": normalize_text(metadata.get("description")),
        "author": normalize_text(metadata.get("author")),
        "published": metadata.get("published"),
        "image": metadata.get("image"),
        "category": topic or metadata.get("category"),
        "tags": metadata.get("tags") or [],
        "content": content,
        "url": metadata.get("url") or url,
        "scraped_at": datetime.now(timezone.utc).isoformat(),
    }


def scrape(topic: Optional[str] = None, known_urls: Optional[Set[str]] = None) -> list[dict]:
    """Scrape News24 listing pages and return normalized article dictionaries."""
    session = build_session()
    known = known_urls or set()
    seen_urls: Set[str] = set()
    items: list[dict] = []

    topics = {topic: TOPIC_URLS[topic]} if topic else TOPIC_URLS
    logger.info("%s scraper started for topics=%s", SOURCE_NAME, list(topics.keys()))

    for topic_name, topic_url in topics.items():
        html = fetch_url(session=session, url=topic_url, logger=logger)
        if not html:
            continue

        soup = BeautifulSoup(html, "html.parser")
        links = extract_links_from_listing(soup=soup, base_url=BASE_URL, listing_url=topic_url)
        logger.info("%s topic=%s links discovered=%s", SOURCE_NAME, topic_name, len(links))

        for link in links:
            if link in seen_urls or link in known:
                continue
            seen_urls.add(link)

            try:
                article = _scrape_article_with_session(session=session, url=link, topic=topic_name)
                if article:
                    items.append(article)
            except Exception as exc:  # pragma: no cover
                logger.exception("%s article scrape failed for %s: %s", SOURCE_NAME, link, exc)

    logger.info("%s scraper finished. articles=%s", SOURCE_NAME, len(items))
    return items
