#!/usr/bin/env python3
""" API v1 for performances CRUD """


from backend.models import storage
from backend.models.employee import Employee
from backend.models.performance import Performance
from backend.api.v1.views import app_views
from flask import jsonify, request, abort
from sqlalchemy.exc import IntegrityError


@app_views.get('/employees/<employee_id>/performances')
def get_employee_performances(employee_id):
    """ Retrieves all performances of a specific employee """
    employee = storage.get(Employee, employee_id)
    if not employee:
        abort(404)

    return jsonify(
        [performance.to_dict() for performance in employee.performance]
    )


@app_views.get('/performances/<performance_id>')
def get_performances(performance_id):
    """ Retrieves a specific performance """
    performance = storage.get(Performance, performance_id)
    if not performance:
        abort(404)

    return jsonify(performance.to_dict())


@app_views.post('/employees/<employee_id>/performances')
def create_performance(employee_id):
    """ Creates a new performance """
    employee = storage.get(Employee, employee_id)
    if not employee:
        abort(404)

    data = request.get_json(force=True)
    if not data:
        abort(400, 'Not a valid JSON')
    if 'score' not in data:
        abort(400, 'Missing score')

    data['employee_id'] = employee_id
    performance = Performance(**data)

    try:
        storage.new(performance)
    except IntegrityError:
        abort(400, 'Invalid data')
    finally:
        storage.save()

    return jsonify(performance.to_dict()), 201


@app_views.put('/performances/<performance_id>')
def update_performance(performance_id):
    """ Updates a performance """
    performance = storage.get(Performance, performance_id)
    if not performance:
        abort(404)

    data = request.get_json(force=True)
    if not data:
        abort(400, 'Not a valid JSON')

    for key, value in data.items():
        if key not in ['score', 'review']:
            abort(400, f'Invalid key {key}')
        setattr(performance, key, value)

    storage.save()
    return jsonify(performance.to_dict())


@app_views.delete('/performances/<performance_id>')
def delete_performance(performance_id):
    """ Deletes a performance """
    performance = storage.get(Performance, performance_id)
    if not performance:
        abort(404)

    storage.delete(performance)
    storage.save()

    return jsonify({})
