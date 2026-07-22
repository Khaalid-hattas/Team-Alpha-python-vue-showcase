from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


class EWNScraper:

    URL = "https://www.ewn.co.za/"

    def _extract_title(self, card, link):
        title = card.select_one("h1, h2, h3, h4")

        if title:
            return title.get_text(" ", strip=True)

        if link:
            return link.get_text(" ", strip=True)

        return ""

    def scrape(self):

        headers = {
            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64)"
            )
        }

        response = requests.get(
            self.URL,
            headers=headers,
            timeout=15
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        articles = []

        # Update these selectors if EWN changes its layout.
        cards = soup.select("article")[:10]

        for card in cards:

            link = card.select_one("a")
            summary = card.select_one("p")

            href = link["href"] if link and link.has_attr("href") else ""

            articles.append({
                "title": self._extract_title(card, link),
                "summary": summary.get_text(" ", strip=True) if summary else "",
                "url": urljoin(self.URL, href) if href else ""
            })

        return articles
