from flask import Blueprint, jsonify, request

search_bp = Blueprint("search", __name__)

@search_bp.route("/api/search", methods=["GET"])
def search():
    try:
        # Get the search query
        query = request.args.get("q")

        # Return an error if no query is provided
        if not query:
            return jsonify({
                "error": "Search query is required."
            }), 400

        # Placeholder for future search results
        results = []

        return jsonify({
            "query": query,
            "results": results
        }), 200

    except Exception:
        return jsonify({
            "error": "An unexpected error occurred."
        }), 500