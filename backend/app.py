"""Flask application factory: registers blueprints, error handlers, CORS,
and bootstraps storage + the background scraping scheduler.
"""

from __future__ import annotations

import logging
import os
import sys

# Hack to make Python find both root imports ('routes') and backend imports ('services')
_current_dir = os.path.dirname(os.path.abspath(__file__))
_parent_dir = os.path.dirname(_current_dir)
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)
if _current_dir not in sys.path:
    sys.path.insert(0, _current_dir)

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

from routes.articles import articles_bp
from routes.export import export_bp
from routes.health import health_bp
from routes.history import history_bp
from routes.pages import pages_bp
from routes.scrape import scrape_bp
from routes.statistics import statistics_bp
from routes.websites import websites_bp
from services.scraper_service import get_registry_metadata, start_scheduler
from services.storage import init_storage, seed_websites
from utils.errors import register_error_handlers

load_dotenv()


def configure_logging() -> None:
    """Set baseline logging format and level."""
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO"),
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )


def create_app() -> Flask:
    configure_logging()
    logger = logging.getLogger(__name__)

    app = Flask(__name__)
    app.config["JSON_SORT_KEYS"] = False
    CORS(app, origins=[os.getenv("CORS_ORIGIN", "http://localhost:5173")])

    register_error_handlers(app)

    for blueprint in (
        pages_bp,
        health_bp,
        scrape_bp,
        articles_bp,
        statistics_bp,
        history_bp,
        websites_bp,
        export_bp,
    ):
        app.register_blueprint(blueprint)

    # Bootstrap storage, seed the website registry from the scraper registry,
    # and start the background refresh scheduler.
    init_storage()
    seed_websites(get_registry_metadata())
    start_scheduler()
    logger.info("Application bootstrap complete")

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False)