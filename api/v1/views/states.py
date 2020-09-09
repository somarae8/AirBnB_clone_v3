#!/usr/bin/python3

from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def list_states():
    list_states = []
    get_state = storage.all(State)
    for k, v in get_state.items():
        list_states.append(v.to_dict())
    return jsonify(list_states)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def state(state_id=None):
    get_state = {}
    if state_id:
        get_state = storage.get(State, state_id)

    if get_state is None:
        return abort(404)

    return jsonify(get_state.to_dict())


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def del_state(state_id=None):
    get_state = storage.get(State, state_id)
    if get_state:
        print(get_state)
        storage.delete(get_state)
        storage.save()
    else:
        return abort(404)
    return jsonify({}), 200


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def add_state():
    if not request.json:
        abort(400, 'Not a JSON')

    if not 'name' in request.json:
        abort(400, 'Missing name')

    new_s = State()
    data = dict(request.get_json(silent=True))
    new_s.name = data['name']

    storage.new(new_s)
    storage.save()
    storage.reload()

    return jsonify(new_s.to_dict())


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_state(state_id=None):

    if not request.json:
        abort(400, 'Not a JSON')

    get_state = storage.get(State, state_id)

    if get_state:
        update_s = dict(request.get_json(silent=True))
        for k, v in update_s.items():
            setattr(get_state, k, v)

        print(get_state.to_dict())
        storage.save()
    else:
        return abort(404)

    return jsonify({"update": "OK"}), 200
