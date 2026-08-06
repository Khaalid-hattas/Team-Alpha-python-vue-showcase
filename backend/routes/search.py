from flask import Blueprint, jsonify, request
from services.storage import get_articles

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

        # Updated
        query = query.lower()

        articles = get_articles(limit=500)

        results = []

        for article in articles:
            title = (article.get("title") or "").lower()
            summary = (article.get("summary") or "").lower()
            description = (article.get("description") or "").lower()

            if (
                query in title
                or query in summary
                or query in description
            ):
                results.append(article)

        return jsonify({
            "query": query,
            "count": len(results),
            "results": results
        }), 200

    except Exception as e:
        return jsonify({
            "error": "An unexpected error occurred.",
            "details": str(e)
        }), 500