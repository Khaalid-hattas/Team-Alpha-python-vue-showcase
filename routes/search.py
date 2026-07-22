from flask import Blueprint, jsonify, request

search_bp = Blueprint("search", __name__)


@search_bp.route("/api/search")
def search():

    keyword = request.args.get("q", "")

    return jsonify({
        "query": keyword,
        "results": []
    })