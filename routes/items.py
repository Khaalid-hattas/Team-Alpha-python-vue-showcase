from flask import Blueprint, jsonify

# Create a Blueprint for the items routes
items_bp = Blueprint("items", __name__)

# Endpoint to return all scraped items
@items_bp.route("/api/items")
def get_items():

    # Return an empty list until scraped data is available
    return jsonify([]), 200  # HTTP 200 = Request successful