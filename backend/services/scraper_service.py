"""Scraper orchestration, registry, and scheduled refresh management."""

from __future__ import annotations

import logging
import os
import time
from datetime import datetime, timezone
from typing import Callable, Optional

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.base import STATE_RUNNING

from scrapers import ewn_scraper, news24_scraper, sabc_scraper
from services.storage import get_all_urls, get_article_count, normalize_item, save_items

logger = logging.getLogger(__name__)

REFRESH_INTERVAL_MINUTES = int(os.getenv("SCRAPER_REFRESH_MINUTES", "15"))

ScraperCallable = Callable[[Optional[set[str]]], list[dict]]


def _wrap_topic_scrape(scrape_func, topic: str) -> ScraperCallable:
    def runner(known_urls: Optional[set[str]] = None) -> list[dict]:
        return scrape_func(topic=topic, known_urls=known_urls)

    return runner


SCRAPER_REGISTRY: dict[str, ScraperCallable] = {
    "ewn_latest": _wrap_topic_scrape(ewn_scraper.scrape, "latest"),
    "ewn_local": _wrap_topic_scrape(ewn_scraper.scrape, "local"),
    "ewn_politics": _wrap_topic_scrape(ewn_scraper.scrape, "politics"),
    "ewn_world": _wrap_topic_scrape(ewn_scraper.scrape, "world"),
    "news24_latest": _wrap_topic_scrape(news24_scraper.scrape, "latest"),
    "news24_business": _wrap_topic_scrape(news24_scraper.scrape, "business"),
    "news24_sport": _wrap_topic_scrape(news24_scraper.scrape, "sport"),
    "news24_investigations": _wrap_topic_scrape(news24_scraper.scrape, "investigations"),
    "sabc_top": _wrap_topic_scrape(sabc_scraper.scrape, "top"),
    "sabc_opinion": _wrap_topic_scrape(sabc_scraper.scrape, "opinion"),
    "sabc_sport": _wrap_topic_scrape(sabc_scraper.scrape, "sport"),
}


scheduler = BackgroundScheduler(timezone="UTC")
_last_refresh_at: Optional[str] = None
_last_duration_seconds: Optional[float] = None


def scrape_all_sources(force_full: bool = False) -> dict:
    """Run all registered scrapers, normalize items, and persist new content."""
    global _last_refresh_at, _last_duration_seconds

    start_ts = time.perf_counter()
    logger.info("Scrape refresh started. force_full=%s", force_full)

    seen_urls = set() if force_full else get_all_urls()
    total_found = 0
    total_errors = 0
    all_normalized: list[dict] = []

    for name, scraper_runner in SCRAPER_REGISTRY.items():
        scraper_start = time.perf_counter()
        logger.info("Scraper started: %s", name)
        try:
            items = scraper_runner(seen_urls)
            total_found += len(items)

            normalized = [normalize_item(item) for item in items]
            normalized = [item for item in normalized if item.get("url")]

            for item in normalized:
                seen_urls.add(item["url"])

            all_normalized.extend(normalized)
            logger.info(
                "Scraper finished: %s articles=%s duration=%.2fs",
                name,
                len(normalized),
                time.perf_counter() - scraper_start,
            )
        except Exception as exc:  # pragma: no cover
            total_errors += 1
            logger.exception("Scraper failed: %s error=%s", name, exc)

    save_result = save_items(all_normalized)

    _last_refresh_at = datetime.now(timezone.utc).isoformat()
    _last_duration_seconds = time.perf_counter() - start_ts

    logger.info(
        "Scrape refresh finished. found=%s saved=%s duplicates=%s errors=%s duration=%.2fs",
        total_found,
        save_result["saved"],
        save_result["duplicates"],
        total_errors,
        _last_duration_seconds,
    )

    return {
        "found": total_found,
        "saved": save_result["saved"],
        "duplicates": save_result["duplicates"],
        "errors": total_errors,
        "duration_seconds": round(_last_duration_seconds, 3),
        "last_refresh": _last_refresh_at,
    }


def _safe_scheduled_refresh() -> None:
    """Run scheduled refresh without allowing an exception to kill scheduler loop."""
    try:
        scrape_all_sources(force_full=False)
    except Exception as exc:  # pragma: no cover
        logger.exception("Scheduled refresh failed: %s", exc)


def start_scheduler() -> None:
    """Start APScheduler periodic refresh job."""
    if scheduler.running:
        return

    scheduler.add_job(
        _safe_scheduled_refresh,
        trigger="interval",
        minutes=REFRESH_INTERVAL_MINUTES,
        id="news_refresh",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )
    scheduler.start()
    logger.info("Scheduler started. interval_minutes=%s", REFRESH_INTERVAL_MINUTES)


def get_scheduler_status() -> dict:
    """Return scheduler and scraper runtime status."""
    return {
        "running": scheduler.state == STATE_RUNNING,
        "interval_minutes": REFRESH_INTERVAL_MINUTES,
        "last_refresh": _last_refresh_at,
        "last_duration_seconds": _last_duration_seconds,
        "stored_articles": get_article_count(),
        "sources_registered": sorted(SCRAPER_REGISTRY.keys()),
    }

def get_registry_metadata() -> list[dict]:
    """Return metadata about registered scrapers."""
    return [{"name": name, "url": ""} for name in SCRAPER_REGISTRY.keys()]
