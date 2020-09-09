#!/usr/bin/python3
"""routes of State """
from api.v1.views import app_views
from flask import Flask, jsonify, abort
from models import storage
from models.cities import City
from models.state import State


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['GET'])
def list_citys_of_a_states(state_id=None):
    """search cities with states_id"""
    city_list = []
    state_obj = storage.get(State, state_id)

    if state_obj is None:
        abort(404)
    for obj in state_obj.cities:
        city_list.append(obj.to_dict())

    return jsonify(city_list)


@app_views.route('cities/<city_id>', strict_slashes=False, methods=['GET'])
def list_a_city(city_id=None):
    """search a city with city_id"""
    if city_id:
        city_obj = storage.get(City, city_id)

    if city_obj is None:
        abort(404)
    return jsonify(city_obj.to_dict())


@app_views.route('cities/<city_id>', strict_slashes=False, methods=['DELETE'])
def del_a_city(city_id=None):
    """delete cities with states_id"""
    if city_id:
        city_obj = storage.get(City, city_id)

    if city_obj is None:
        abort(404)
    storage.delete(fetched_obj)
    storage.save()


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def create_a_city(state_id=None):
    """create a city"""
    if states_id is None:
        abort(404)
    the_json = request.get_json(silent=True)
    if the_json is None:
        abort(400, 'Not a JSON')

    elif 'name' not in json:
        return jsonify({'error': 'Missing name'}), 400
    else:
        city_new = City(**json_request)
        city_new.state_id = state_id
        storage.new(city_new)
        storage.save()
        return jsonify(city_new.to_dict()), 201


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['PUT'])
def update_cities(city_id):
    """Updates a City"""
    if city_id is None:
        abort(404)
    json = request.get_json()
    if not json:
        return jsonify({'error': 'Not a JSON'}), 400
    cities_id = storage.get("City", city_id)
    if cities_id:
        for key, value in json.items():
            setattr(cities_id, key, value)
        storage.save()
        return jsonify(cities_id.to_dict()), 200
    else:
        abort(404)
