from flask import Flask
from routes.scrape_routes import scrape_bp
from services.storage_service import init_db


def create_app():
    app = Flask(__name__)
    init_db()
    app.register_blueprint(scrape_bp)
    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)