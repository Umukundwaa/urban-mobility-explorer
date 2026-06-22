from flask import Flask
from flask_cors import CORS
from api.trips_routes import trips_bp
from api.zones_routes import zones_bp
from api.insights_routes import insights_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(trips_bp)
app.register_blueprint(zones_bp)
app.register_blueprint(insights_bp)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
