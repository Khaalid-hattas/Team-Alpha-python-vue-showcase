from flask import Blueprint, jsonify

websites_bp = Blueprint("websites", __name__)


@websites_bp.route("/api/websites")
def websites():
    return jsonify([
        "Nike",
        "News24",
        "Takealot"
    ])