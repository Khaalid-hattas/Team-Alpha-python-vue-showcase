"""Shared scraping utilities for resilient, polite multi-source scraping."""

from __future__ import annotations

import logging
import re
import time
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, Optional, Set
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup, Tag
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

REQUEST_DELAY_SECONDS = 0.5
DEFAULT_TIMEOUT_SECONDS = 15
DEFAULT_USER_AGENT = (
    "TeamAlphaNewsBot/1.0 (+https://example.local/team-alpha; contact=team-alpha@example.com)"
)

_ROBOTS_CACHE: Dict[str, RobotFileParser] = {}


def build_session() -> requests.Session:
    """Build an HTTP session with conservative retry/backoff behavior."""
    session = requests.Session()
    retry = Retry(
        total=3,
        connect=3,
        read=3,
        backoff_factor=0.75,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset(["GET"]),
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session.headers.update({"User-Agent": DEFAULT_USER_AGENT})
    return session


def _robots_for_url(
    session: requests.Session,
    url: str,
    logger: Optional[logging.Logger] = None,
) -> Optional[RobotFileParser]:
    parsed = urlparse(url)
    root = f"{parsed.scheme}://{parsed.netloc}"
    if root in _ROBOTS_CACHE:
        return _ROBOTS_CACHE[root]

    robots_url = f"{root}/robots.txt"
    parser = RobotFileParser()
    parser.set_url(robots_url)

    try:
        response = session.get(robots_url, timeout=DEFAULT_TIMEOUT_SECONDS)
        if response.ok:
            parser.parse(response.text.splitlines())
            _ROBOTS_CACHE[root] = parser
            return parser
        if logger:
            logger.warning("robots.txt unavailable (%s): %s", robots_url, response.status_code)
    except requests.RequestException as exc:
        if logger:
            logger.warning("robots.txt fetch failed for %s: %s", robots_url, exc)
    return None


def can_fetch(
    session: requests.Session,
    url: str,
    user_agent: str = DEFAULT_USER_AGENT,
    logger: Optional[logging.Logger] = None,
) -> bool:
    """Check robots.txt rules; if unavailable, allow scraping."""
    parser = _robots_for_url(session=session, url=url, logger=logger)
    if parser is None:
        return True
    try:
        return parser.can_fetch(user_agent, url)
    except Exception:
        return True


def fetch_url(
    session: requests.Session,
    url: str,
    logger: Optional[logging.Logger] = None,
    timeout: int = DEFAULT_TIMEOUT_SECONDS,
) -> Optional[str]:
    """Fetch URL safely with robots checking, timeout, retries, and pacing."""
    if not can_fetch(session=session, url=url, logger=logger):
        if logger:
            logger.info("Blocked by robots.txt: %s", url)
        time.sleep(REQUEST_DELAY_SECONDS)
        return None

    try:
        response = session.get(url, timeout=timeout)
        if response.ok:
            return response.text
        if logger:
            logger.warning("Request failed [%s] %s", response.status_code, url)
        return None
    except requests.RequestException as exc:
        if logger:
            logger.error("Request error for %s: %s", url, exc)
        return None
    finally:
        time.sleep(REQUEST_DELAY_SECONDS)


def safe_text(node: Optional[Tag]) -> Optional[str]:
    """Safely extract text content from a tag."""
    if node is None:
        return None
    text = node.get_text(" ", strip=True)
    return text or None


def _meta_content(
    soup: BeautifulSoup,
    *,
    property_name: Optional[str] = None,
    name: Optional[str] = None,
    itemprop: Optional[str] = None,
) -> Optional[str]:
    attrs: Dict[str, str] = {}
    if property_name:
        attrs["property"] = property_name
    if name:
        attrs["name"] = name
    if itemprop:
        attrs["itemprop"] = itemprop

    tag = soup.find("meta", attrs=attrs)
    if not isinstance(tag, Tag):
        return None
    content = tag.get("content")
    if isinstance(content, str):
        cleaned = content.strip()
        return cleaned or None
    return None


def get_og_value(soup: BeautifulSoup, key: str) -> Optional[str]:
    """Read Open Graph metadata fields from a page."""
    return _meta_content(soup, property_name=f"og:{key}")


def parse_datetime(value: Optional[str]) -> Optional[str]:
    """Best-effort datetime parsing, returns ISO 8601 if possible."""
    if not value:
        return None
    cleaned = value.strip()
    if not cleaned:
        return None
    try:
        if cleaned.endswith("Z"):
            cleaned = cleaned[:-1] + "+00:00"
        return datetime.fromisoformat(cleaned).isoformat()
    except ValueError:
        return cleaned


def extract_canonical_url(soup: BeautifulSoup, fallback_url: str) -> str:
    """Extract canonical URL from page or return fallback URL."""
    canonical = soup.find("link", rel="canonical")
    if isinstance(canonical, Tag):
        href = canonical.get("href")
        if isinstance(href, str) and href.strip():
            return href.strip()
    return fallback_url


def extract_tags(soup: BeautifulSoup) -> list[str]:
    """Extract possible tags/keywords from metadata and page links."""
    tags: Set[str] = set()
    keywords = _meta_content(soup, name="keywords")
    if keywords:
        for part in keywords.split(","):
            value = part.strip()
            if value:
                tags.add(value)

    for anchor in soup.select('a[rel~="tag"], a[href*="/tag/"]'):
        if isinstance(anchor, Tag):
            label = safe_text(anchor)
            if label:
                tags.add(label)
    return sorted(tags)


def extract_article_body(soup: BeautifulSoup) -> Optional[str]:
    """Extract article body text with resilient fallbacks."""
    candidates = [
        soup.find("article"),
        soup.find(attrs={"itemprop": "articleBody"}),
        soup.find("div", class_=re.compile(r"content|article|story|body", re.I)),
    ]

    for candidate in candidates:
        if not isinstance(candidate, Tag):
            continue
        paragraphs = [
            p.get_text(" ", strip=True)
            for p in candidate.find_all("p")
            if isinstance(p, Tag) and p.get_text(" ", strip=True)
        ]
        if paragraphs:
            return "\n\n".join(paragraphs)

    # Last resort: collect all visible paragraph text.
    paragraphs = [
        p.get_text(" ", strip=True)
        for p in soup.find_all("p")
        if isinstance(p, Tag) and p.get_text(" ", strip=True)
    ]
    if paragraphs:
        return "\n\n".join(paragraphs)
    return None


def collect_metadata(soup: BeautifulSoup, article_url: str) -> Dict[str, Any]:
    """Collect common metadata with graceful handling of missing values."""
    title = get_og_value(soup, "title")
    if not title:
        h1 = soup.find("h1")
        title = safe_text(h1)
    if not title and soup.title:
        title = safe_text(soup.title)

    summary = (
        _meta_content(soup, name="description")
        or _meta_content(soup, property_name="description")
        or get_og_value(soup, "description")
    )

    author = (
        _meta_content(soup, name="author")
        or _meta_content(soup, property_name="article:author")
        or _meta_content(soup, itemprop="author")
    )

    published = parse_datetime(
        _meta_content(soup, property_name="article:published_time")
        or _meta_content(soup, name="article:published_time")
        or _meta_content(soup, itemprop="datePublished")
        or _meta_content(soup, property_name="og:updated_time")
    )

    category = (
        _meta_content(soup, property_name="article:section")
        or _meta_content(soup, name="section")
        or _meta_content(soup, itemprop="articleSection")
    )

    return {
        "title": title,
        "summary": summary,
        "description": get_og_value(soup, "description") or summary,
        "author": author,
        "published": published,
        "category": category,
        "tags": extract_tags(soup),
        "image": get_og_value(soup, "image"),
        "url": extract_canonical_url(soup, article_url),
    }


def is_probable_article_url(url: str, base_url: str) -> bool:
    """Heuristic filter for article-like URLs from listing pages."""
    parsed = urlparse(url)
    base = urlparse(base_url)
    if not parsed.scheme.startswith("http"):
        return False
    if parsed.netloc != base.netloc:
        return False
    if parsed.fragment:
        return False

    path = parsed.path.lower().strip("/")
    if not path:
        return False
    if any(
        skip in path
        for skip in (
            "/video",
            "/podcast",
            "/photos",
            "/gallery",
            "/live",
            "privacy",
            "contact",
            "advert",
        )
    ):
        return False

    tokens = path.split("/")
    if len(tokens) >= 3:
        return True
    return bool(re.search(r"\d{4}|article|story|news", path))


def extract_links_from_listing(
    soup: BeautifulSoup,
    base_url: str,
    listing_url: str,
) -> Set[str]:
    """Extract unique article links from a topic/listing page."""
    links: Set[str] = set()
    for anchor in soup.find_all("a", href=True):
        href = anchor.get("href")
        if not isinstance(href, str):
            continue
        absolute = urljoin(listing_url, href.strip())
        if is_probable_article_url(absolute, base_url):
            links.add(absolute)
    return links


def utc_now_iso() -> str:
    """UTC now in ISO format."""
    return datetime.now(timezone.utc).isoformat()


def normalize_text(value: Optional[str]) -> Optional[str]:
    """Normalize whitespace in text fields."""
    if value is None:
        return None
    cleaned = re.sub(r"\s+", " ", value).strip()
    return cleaned or None
