#!/usr/bin/env python3
"""API For users crud """


from backend.models.api.v1.views import app_views
from backend.models import storage
from backend.models.user import User
from flask import jsonify, request, abort
from sqlalchemy.exc import IntegrityError


@app_views.route('/users', methods=['GET'])
def get_users():
    """ get all users in db """
    users = storage.all(User)
    return jsonify([user.to_dict() for user in users.values()])


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """ get user by id """
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    abort(404)


@app_views.route('/users', methods=['POST'])
def create_user():
    """ create user """
    data = request.get_json(force=True)
    if not data:
        abort(400, 'Not a JSON')
    if 'email' not in data or data['email'] == '':
        abort(400, 'Missing email')
    if 'password' not in data or data['password'] == '':
        abort(400, 'Missing password')
    if 'userName' not in data or data['userName'] == '':
        abort(400, 'Missing userName')

    user = User(**data)
    users = storage.all(User)
    if not users:
        user.manager = True
    for u in users.values():
        if u.email == user.email:
            abort(400, 'Email already exists')
        if u.userName == user.userName:
            abort(400, 'userName already exists')
    try:
        user.save()
    except IntegrityError as e:
        abort(400, str(e))
    finally:
        return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """ update user by id """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['email', 'password', 'userName', 'name', 'manager']:
            continue
        # need to validate email for auth
        setattr(user, key, value)

    try:
        user.save()
    except IntegrityError as e:
        abort(400, str(e))
    finally:
        return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """ delete user by id """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 204
