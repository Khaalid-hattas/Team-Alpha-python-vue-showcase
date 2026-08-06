from flask import Blueprint, jsonify, request
from services.storage import get_articles

# Create a Blueprint for the items routes
items_bp = Blueprint("items", __name__)

# Endpoint to return all scraped items
@items_bp.route("/api/items", methods=["GET"])
def get_items():

    limit = int(request.args.get("limit", 100))
    source = request.args.get("source")
    
    article = get_articles(limit=limit, source=source)  # Default limit to 100 if not provided

    # Return an empty list until scraped data is available
    
    return jsonify({
        "status": "success",
        "count": len(article),
        "items": article
    }), 200 # HTTP 200 = Request successful