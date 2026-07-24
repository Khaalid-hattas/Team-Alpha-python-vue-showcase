from scrapers.ewn_scraper import EWNScraper, SOURCE_NAME
from scrapers.news24_scraper import News24Scraper
from services.storage_service import save_items


def normalize_item(item):
    title = (item.get("title") or "").strip()
    summary = (item.get("summary") or item.get("description") or "").strip()

    if summary == title:
        summary = ""

    return {
        "source": (item.get("source") or SOURCE_NAME).strip(),
        "topic": (item.get("topic") or "").strip(),
        "title": title,
        "summary": summary,
        "description": (item.get("description") or summary).strip(),
        "author": (item.get("author") or "").strip(),
        "image": (item.get("image") or "").strip(),
        "tags": item.get("tags") or [],
        "url": (item.get("url") or "").strip(),
    }


class ScrapeService:

    def __init__(self):
        self.ewn_scraper = EWNScraper()
        self.news24_scraper = News24Scraper()
        self.SCRAPER_REGISTRY = {
            "ewn_latest": lambda limit: self.ewn_scraper.scrape("ewn_latest", limit),
            "ewn_local": lambda limit: self.ewn_scraper.scrape("ewn_local", limit),
            "ewn_politics": lambda limit: self.ewn_scraper.scrape("ewn_politics", limit),
            "ewn_world": lambda limit: self.ewn_scraper.scrape("ewn_world", limit),
            "news24_latest": lambda limit: self.news24_scraper.scrape("news24_latest", limit),
        }

    def scrape_news(self, topic="ewn_latest", limit=10):
        if topic not in self.SCRAPER_REGISTRY:
            raise ValueError(f"Unknown topic '{topic}'.")

        raw_items = self.SCRAPER_REGISTRY[topic](limit)
        normalized_items = [
            normalize_item(item)
            for item in raw_items
            if item and item.get("url")
        ]

        return save_items(normalized_items)
