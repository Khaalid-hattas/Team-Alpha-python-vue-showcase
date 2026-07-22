from flask import Blueprint, jsonify

# Create a Blueprint for the health check route
health_bp = Blueprint("health", __name__)

# Endpoint to check if the backend API is running
@health_bp.route("/api/health")
def health():

    # Return the current health status of the backend
    return jsonify({
        "status": "healthy",
        "message": "Backend is running"
    }), 200  # HTTP 200 = Request successful