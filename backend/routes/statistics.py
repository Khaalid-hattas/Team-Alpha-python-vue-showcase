from flask import Blueprint, jsonify
from services.scraper_service import get_scheduler_status #fetches from scraper service

# Create a Blueprint for the statistics routes
statistics_bp = Blueprint("statistics", __name__)

# Endpoint to return dashboard statistics added the GET METHOD
@statistics_bp.route("/api/statistics", methods=["GET"])
def statistics():

    # Updated  removed place holder
    return jsonify(get_scheduler_status()), 200