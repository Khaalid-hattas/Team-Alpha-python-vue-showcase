from flask import Blueprint, jsonify

history_bp = Blueprint("history", __name__)


@history_bp.route("/api/history")
def history():
    return jsonify([])