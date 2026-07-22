from flask import Blueprint, jsonify

statistics_bp = Blueprint("statistics", __name__)


@statistics_bp.route("/api/statistics")
def statistics():
    return jsonify({
        "total_items": 0,
        "total_websites": 0
    })