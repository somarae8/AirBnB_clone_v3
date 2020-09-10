#!/usr/bin/python3
"""
Create view routes for amenities
"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities',
                 strict_slashes=False, methods=['GET'])
def list_amenities():
    """list amenities"""
    list_amenities = []
    get_amenity = storage.all(Amenity)
    for k, v in get_amenity.items():
        list_amenities.append(v.to_dict())
    return jsonify(list_amenities)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET'])
def amenity(amenity_id=None):
    """list amenities"""
    get_amenity = {}
    if amenity_id:
        get_amenity = storage.get(Amenity, amenity_id)

    if get_amenity is None:
        return abort(404)

    return jsonify(get_amenity.to_dict()), 200


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['DELETE'])
def del_amenity(amenity_id=None):
    """delete amenities"""

    get_amenity = storage.get(amenity, amenity_id)
    if get_amenity:
        storage.delete(get_amenity)
        storage.save()
        return jsonify({}), 200
    else:
        return abort(404)


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def add_amenity():
    """add amenity"""
    if not request.get_json(silent=True):
        return jsonify({'error': 'Not a JSON'}), 400

    if 'name' not in request.json:
        abort(400, 'Missing name')

    new_a = Amenity()
    data = dict(request.get_json(silent=True))
    new_a.name = data['name']

    storage.new(new_a)
    storage.save()
    storage.reload()

    return jsonify(new_a.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['PUT'])
def update_amenity(amenity_id=None):
    """update amenity"""

    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400

    get_amenity = storage.get(Amenity, amenity_id)

    if get_amenity:
        update_s = dict(request.get_json(silent=True))
        for k, v in update_s.items():
            setattr(get_amenity, k, v)
        storage.save()
    else:
        abort(404)

    return jsonify(get_amenity.to_dict()), 200
