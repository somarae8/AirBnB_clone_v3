#!/usr/bin/python3
"""
Create view route for states
"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def list_states():
    """list states"""
    list_states = []
    get_state = storage.all(State)
    for k, v in get_state.items():
        list_states.append(v.to_dict())
    return jsonify(list_states)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def state(state_id=None):
    """list states"""
    get_state = {}
    if state_id:
        get_state = storage.get(State, state_id)

    if get_state is None:
        return abort(404)

    return jsonify(get_state.to_dict()), 200


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def del_state(state_id=None):
    """delete states"""

    get_state = storage.get(State, state_id)
    if get_state:
        storage.delete(get_state)
        storage.save()
        return jsonify({}), 200
    else:
        return abort(404)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def add_state():
    """add state"""
    if not request.get_json(silent=True):
        return jsonify({'error': 'Not a JSON'}), 400

    if not 'name' in request.json:
        abort(400, 'Missing name')

    new_s = State()
    data = dict(request.get_json(silent=True))
    new_s.name = data['name']

    storage.new(new_s)
    storage.save()
    storage.reload()

    return jsonify(new_s.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_state(state_id=None):
    """update states"""

    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400

    get_state = storage.get(State, state_id)

    if get_state:
        update_s = dict(request.get_json(silent=True))
        for k, v in update_s.items():
            setattr(get_state, k, v)

        storage.save()
    else:
        abort(404)

    return jsonify(get_state.to_dict()), 200
