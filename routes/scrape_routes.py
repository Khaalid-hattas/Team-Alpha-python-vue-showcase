from flask import Blueprint, jsonify, request
from services.scrape_service import ScrapeService
from services.storage_service import get_items

scrape_bp = Blueprint("scrape", __name__)

service = ScrapeService()


def _as_bool(value):
    if value is None:
        return False

    return value.strip().lower() in {"1", "true", "yes", "on"}


@scrape_bp.route("/api/scrape", methods=["GET"])
def scrape():
    topic = request.args.get("topic", "ewn_latest")
    limit = request.args.get("limit", default=10, type=int)

    if limit < 1:
        return jsonify({"error": "limit must be >= 1"}), 400

    try:
        news = service.scrape_news(topic=topic, limit=limit)
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    return jsonify(news)


@scrape_bp.route("/api/items", methods=["GET"])
def list_items():
    topic = request.args.get("topic", "ewn_latest")
    source = request.args.get("source")
    limit = request.args.get("limit", default=20, type=int)
    live = _as_bool(request.args.get("live"))

    if limit < 1:
        return jsonify({"error": "limit must be >= 1"}), 400

    if live:
        try:
            service.scrape_news(topic=topic, limit=limit)
        except ValueError as error:
            return jsonify({"error": str(error)}), 400

    items = get_items(topic=topic, source=source, limit=limit)
    return jsonify(items)