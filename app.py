from flask import Flask
from routes.scrape_routes import scrape_bp

app = Flask(__name__)

app.register_blueprint(scrape_bp)

if __name__ == "__main__":
    app.run(debug=True)