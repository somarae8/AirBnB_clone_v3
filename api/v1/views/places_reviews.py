#!/usr/bin/python3
"""routes of Places """
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['GET'])
def list_views_of_a_place(place_id=None):
    """search views with place"""
    review_list = []
    review_obj = storage.get(Place, place_id)

    if review_obj:
        for obj in review_obj.reviews:
            review_list.append(obj.to_dict())
        return jsonify(review_list)
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['GET'])
def list_a_review(review_id=None):
    """search a review with review_id"""
    if review_id:
        review_obj = storage.get(Review, review_id)

    if review_obj:
        return jsonify(review_obj.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['DELETE'])
def del_a_review(review_id=None):
    """delete review with review_id"""
    if review_id:
        review_obj = storage.get(Review, review_id)

    if review_obj:
        storage.delete(review_obj)
        storage.save()
        return (jsonify({})), 200
    else:
        abort(404)


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def create_a_review(place_id=None):
    """create a review with place_id"""
    if place_id is None:
        abort(404)

    get_place = storage.get(Place, place_id)
    if get_place is None:
        abort(404)

    data = request.get_json(silent=True)

    if not data:
        return jsonify({'error': 'Not a JSON'}), 400

    get_user = storage.get(User, data['user_id'])
    if get_user is None:
        abort(404)
    if 'text' not in request.json:
        abort(400, 'Missing text')

    review_new = Review(**data)
    review_new.place_id = place_id
    review_new.user_id = data['user_id']
    storage.new(review_new)
    storage.save()
    return jsonify(review_new.to_dict()), 201


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['PUT'])
def update_review(review_id=None):
    """Updates a review"""
    if review_id is None:
        abort(404)
    json = request.get_json(silent=True)
    if not json:
        return jsonify({'error': 'Not a JSON'}), 400

    get_review = storage.get(Review, review_id)
    if get_review:
        for key, value in json.items():
            setattr(get_review, key, value)
        storage.save()
        return jsonify(get_review.to_dict()), 200
    else:
        abort(404)
