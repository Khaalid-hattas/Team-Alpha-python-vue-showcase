from flask import Blueprint, jsonify

# Create a Blueprint for the history routes
history_bp = Blueprint("history", __name__)

# Endpoint to return the scraping history
@history_bp.route("/api/history")
def history():

    #updated return message to indicate that scrape history is not yet implemented   
    # Return an empty list until scrape history is implemented
    return jsonify({
        "message": "Scrape history is not yet implemented."
    }), 200 # HTTP 200 = Request successful