from flask import Blueprint, jsonify

# Create a Blueprint for the websites routes
websites_bp = Blueprint("websites", __name__)

# Endpoint to return the list of supported websites
@websites_bp.route("/api/websites")
def websites():

    # Return the websites that can be scraped
    return jsonify([
        "Nike",
        "News24",
        "Takealot"
    ]), 200  # HTTP 200 = Request successful