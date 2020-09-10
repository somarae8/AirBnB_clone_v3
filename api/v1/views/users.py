#!/usr/bin/python3
"""
Create view routes for users
"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.users import User


@app_views.route('/users',
                 strict_slashes=False, methods=['GET'])
def list_users():
    """list users"""
    list_users = []
    get_users = storage.all(User)
    for k, v in get_users.items():
        list_users.append(v.to_dict())
    return jsonify(list_users)


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['GET'])
def user(user_id=None):
    """list user"""
    get_user = {}
    if user_id:
        get_user = storage.get(User, user_id)

    if get_user is None:
        return abort(404)

    return jsonify(get_user.to_dict()), 200


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['DELETE'])
def del_user(user_id=None):
    """delete users"""

    user_id = storage.get(User, user_id)
    if user_id:
        storage.delete(user_id)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def add_user():
    """add user"""
    if not request.get_json(silent=True):
        return jsonify({'error': 'Not a JSON'}), 400

    if 'email' not in request.json:
        abort(400, 'Missing email')
    if 'password' not in request.json:
        abort(400, 'Missing password')

    new_u = User()
    data = dict(request.get_json(silent=True))
    new_u.email = data['email']
    new_u.password = data['password']

    storage.new(new_u)
    storage.save()
    storage.reload()

    return jsonify(new_u.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['PUT'])
def update_user(user_id=None):
    """update user"""

    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400

    get_user = storage.get(User, user_id)

    if get_user:
        update_u = dict(request.get_json(silent=True))
        for k, v in update_u.items():
            setattr(get_user, k, v)
        storage.save()
    else:
        abort(404)

    return jsonify(get_amenity.to_dict()), 200
