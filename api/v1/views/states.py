#!/usr/bin/env python3

from api.v1.views import app_views
from flask import Flask, jsonify, abort
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

@app_views.route('/states/<state_id>', strict_slashes=False, methods=['DELETE'])
def del_state(state_id=None):
    get_state = {}
    if state_id:
        get_state = storage.get(State, state_id)
    if get_state is None:
        return abort(404)
    storage.delete(get_state.to_dict())
    return jsonify({}), 200