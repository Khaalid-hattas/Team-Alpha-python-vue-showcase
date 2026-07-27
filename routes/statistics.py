from flask import Blueprint, jsonify

# Create a Blueprint for the statistics routes
statistics_bp = Blueprint("statistics", __name__)

# Endpoint to return dashboard statistics
@statistics_bp.route("/api/statistics")
def statistics():

    # Return placeholder statistics until real data is connected
    return jsonify({
        "total_items": 0,
        "total_websites": 0
    }), 200  # HTTP 200 = Request successful