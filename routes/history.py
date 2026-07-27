from flask import Blueprint, jsonify

# Create a Blueprint for the history routes
history_bp = Blueprint("history", __name__)

# Endpoint to return the scraping history
@history_bp.route("/api/history")
def history():

    # Return an empty list until scrape history is implemented
    return jsonify([]), 200  # HTTP 200 = Request successful