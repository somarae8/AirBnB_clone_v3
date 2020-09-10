#!/usr/bin/python3
"""routes of Places """
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.city import City
from models.user import User
from models.place import Place


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['GET'])
def list_places_of_a_cities(city_id=None):
    """search places with city_id"""
    place_list = []
    city_obj = storage.get(City, city_id)

    if city_obj:
        for obj in city_obj.places:
            place_list.append(obj.to_dict())
        return jsonify(place_list)
    else:
        abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['GET'])
def list_a_place(place_id=None):
    """search a place with place_id"""
    if place_id:
        place_obj = storage.get(Place, place_id)

    if place_obj:
        return jsonify(place_obj.to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['DELETE'])
def del_a_place(place_id=None):
    """delete place with place_id"""
    if place_id:
        place_obj = storage.get(Place, place_id)

    if place_obj:
        storage.delete(place_obj)
        storage.save()
        return (jsonify({})), 200
    else:
        abort(404)


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def create_a_place(city_id=None):
    """create a place"""
    if city_id is None:
        abort(404)

    get_city = storage.get(City, city_id)
    if get_city is None:
        abort(404)

    data = request.get_json(silent=True)

    if not data:
        return jsonify({'error': 'Not a JSON'}), 400

    if 'name' not in request.json:
        abort(400, 'Missing name')

    if 'user_id' not in request.json:
        abort(400, 'Missing user_id')

    get_user = storage.get(User, data['user_id'])
    if get_user is None:
        abort(404)

    place_new = Place(**data)
    place_new.city_id = city_id
    place_new.user_id = data['user_id']
    storage.new(place_new)
    storage.save()
    return jsonify(place_new.to_dict()), 201


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['PUT'])
def update_places(place_id=None):
    """Updates a place"""
    if place_id is None:
        abort(404)
    json = request.get_json(silent=True)
    if not json:
        return jsonify({'error': 'Not a JSON'}), 400

    get_places = storage.get(Place, place_id)
    if get_places:
        for key, value in json.items():
            setattr(get_places, key, value)
        storage.save()
        return jsonify(get_places.to_dict()), 200
    else:
        abort(404)
