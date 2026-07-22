from flask import Blueprint, jsonify

items_bp = Blueprint("items", __name__)


@items_bp.route("/api/items")
def get_items():
    return jsonify([])