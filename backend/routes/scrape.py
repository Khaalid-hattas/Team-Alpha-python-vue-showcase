# Added this new file it will act as bridge

from flask import Blueprint, jsonify, request
from services.scraper_service import scrape_all_sources

scrape_bp = Blueprint("scrape", __name__)

@scrape_bp.route("/api/scrape", methods=["GET"])
def scrape():

    force_full = request.args.get("force_full", "false").lower() == "true"

    result = scrape_all_sources(force_full=force_full)

    return jsonify({
        "status": "success",
        "result": result
    }), 200