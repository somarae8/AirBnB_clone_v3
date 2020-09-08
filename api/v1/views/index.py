from api.v1.views import app_views
from flask import Flask, jsonify


@app_views.route('/status', method=["GET"])
def message():
    """return a json"""
    return jsonify({"status": "OK"})
