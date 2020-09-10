#!/usr/bin/python3
"""init a Flask web application"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
from os import getenv

app = Flask(__name__)
cors = CORS(app, resources={"*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)


@app.teardown_appcontext
def close_db(self):
    """close function"""
    storage.close()


@app.errorhandler(404)
def not_found(e):
    """not found url"""
    return jsonify({"error": "Not found"}), 404


port = getenv("HBNB_API_PORT") or 5000
host = getenv("HBNB_API_HOST") or '0.0.0.0'

if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
