import re
import time
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


SOURCE_NAME = "News24"
BASE_URL = "https://www.news24.com"
TOPIC_URLS = {
    "news24_latest": BASE_URL,
}


class News24Scraper:

    def __init__(self):
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/127.0.0.0 Safari/537.36"
            )
        }

    def _get_soup(self, url):
        response = requests.get(url, headers=self.headers, timeout=20)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")

    def _meta_content(self, soup, *, name=None, prop=None):
        selector = None

        if prop:
            selector = f'meta[property="{prop}"]'
        elif name:
            selector = f'meta[name="{name}"]'

        if not selector:
            return ""

        tag = soup.select_one(selector)
        if tag and tag.has_attr("content"):
            return tag["content"].strip()

        return ""

    def _extract_tags(self, soup):
        tags = []

        for tag in soup.select('meta[property="article:tag"]'):
            if tag.has_attr("content"):
                value = tag["content"].strip()
                if value:
                    tags.append(value)

        if not tags:
            for anchor in soup.select("a[rel='tag'], a[href*='/tag/']"):
                value = anchor.get_text(" ", strip=True)
                if value:
                    tags.append(value)

        deduped = []
        seen = set()
        for value in tags:
            lowered = value.lower()
            if lowered in seen:
                continue
            seen.add(lowered)
            deduped.append(value)

        return deduped

    def _extract_article_links(self, soup, listing_url, limit):
        links = []
        seen = set()
        listing_host = urlparse(listing_url).netloc
        article_pattern = re.compile(r"^/.+-20\d{6}-\d{3,4}$")

        for anchor in soup.select("a[href]"):
            href = anchor.get("href", "").strip()
            if not href:
                continue

            absolute_url = urljoin(BASE_URL, href)
            parsed = urlparse(absolute_url)

            if parsed.netloc != listing_host:
                continue

            if parsed.path in {"", "/"}:
                continue

            if not article_pattern.match(parsed.path):
                continue

            if absolute_url in seen:
                continue

            seen.add(absolute_url)
            links.append(absolute_url)

            if len(links) >= limit:
                break

        return links

    def scrape_article(self, article_url, topic_key):
        soup = self._get_soup(article_url)

        title = self._meta_content(soup, prop="og:title")
        description = self._meta_content(
            soup,
            name="description"
        ) or self._meta_content(soup, prop="og:description")
        author = self._meta_content(soup, name="author") or self._meta_content(
            soup,
            prop="article:author"
        )
        image = self._meta_content(soup, prop="og:image")

        return {
            "source": SOURCE_NAME,
            "topic": topic_key,
            "title": title,
            "summary": description,
            "description": description,
            "author": author,
            "image": image,
            "tags": self._extract_tags(soup),
            "url": article_url,
        }

    def scrape(self, topic_key="news24_latest", limit=10):
        if topic_key not in TOPIC_URLS:
            raise ValueError(f"Unsupported News24 topic: {topic_key}")

        listing_url = TOPIC_URLS[topic_key]
        listing_soup = self._get_soup(listing_url)
        article_urls = self._extract_article_links(listing_soup, listing_url, limit)

        articles = []
        for article_url in article_urls:
            time.sleep(0.5)

            try:
                item = self.scrape_article(article_url, topic_key)
            except requests.RequestException:
                continue

            if item.get("title") and item.get("url"):
                articles.append(item)

        return articles