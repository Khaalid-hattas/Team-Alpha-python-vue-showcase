from scrapers.ewn_scraper import EWNScraper
from utils.cleaner import clean_articles


class ScrapeService:

    def __init__(self):
        self.scraper = EWNScraper()

    def scrape_news(self):

        data = self.scraper.scrape()

        return clean_articles(data)
