from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import logging
import os

# Load environment variables
load_dotenv()

# ============================
# Import Blueprints
# ============================
from routes.health import health_bp
from routes.items import items_bp
from routes.statistics import statistics_bp
from routes.history import history_bp
from routes.search import search_bp
from routes.websites import websites_bp
from routes.scrape import scrape_bp # added new rout  here

# ============================
# Import Services
# ============================
from services.scraper_service import start_scheduler
from services.storage import init_storage

# ============================
# Configure Logging
# ============================
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)

logger = logging.getLogger(__name__)

# ============================
# Create Flask App
# ============================
app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# Enable CORS
CORS(app)

# ============================
# Register Blueprints
# ============================
app.register_blueprint(health_bp)
app.register_blueprint(items_bp)
app.register_blueprint(statistics_bp)
app.register_blueprint(history_bp)
app.register_blueprint(search_bp)
app.register_blueprint(websites_bp)
app.register_blueprint(scrape_bp) # added new rout  here

# ============================
# Home Route
# ============================
@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to Team Alpha Backend API"
    })


# ============================
# Error Handlers
# ============================
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Resource not found"
    }), 404


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "error": "Internal server error"
    }), 500


@app.errorhandler(Exception)
def handle_exception(error):
    return jsonify({
        "error": str(error)
    }), 500


# ============================
# Bootstrap
# ============================
def bootstrap():
    init_storage()
    start_scheduler()
    logger.info("Application bootstrap complete")


bootstrap()


# ============================
# Run Application
# ============================
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "5000")),
        debug=True
    )