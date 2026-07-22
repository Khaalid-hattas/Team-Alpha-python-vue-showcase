from flask import Blueprint, jsonify
from services.scrape_service import ScrapeService

scrape_bp = Blueprint("scrape", __name__)

service = ScrapeService()


@scrape_bp.route("/api/scrape", methods=["GET"])
def scrape():

    news = service.scrape_news()

    return jsonify(news)