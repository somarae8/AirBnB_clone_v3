from api.v1.views import app_views
from flask import Flask, jsonify


@app_views.route('/status', strict_slashes=False, methods=['GET'])
def message():
    """return a json"""
    return jsonify({"status": "OK"}), 200
