from flask import Blueprint, jsonify
from services.scraper_service import SCRAPER_REGISTRY

# Create a Blueprint for the websites routes
websites_bp = Blueprint("websites", __name__)

# Endpoint to return the list of supported websites
@websites_bp.route("/api/websites")
def websites():

    # Return the websites that can be scraped
    return jsonify({
        "sources": sorted(SCRAPER_REGISTRY.keys())
    }),  200  # HTTP 200 = Request successful