from flask import Flask
from flask_cors import CORS

# Import Blueprints
from routes.health import health_bp
from routes.items import items_bp
from routes.statistics import statistics_bp
from routes.history import history_bp
from routes.search import search_bp
from routes.websites import websites_bp

app = Flask(__name__)

# Enable CORS
CORS(app)

# Register Blueprints
app.register_blueprint(health_bp)
app.register_blueprint(items_bp)
app.register_blueprint(statistics_bp)
app.register_blueprint(history_bp)
app.register_blueprint(search_bp)
app.register_blueprint(websites_bp)


@app.route("/")
def home():
    return {
        "message": "Welcome to Team Alpha Backend API"
    }


if __name__ == "__main__":
    app.run(debug=True)