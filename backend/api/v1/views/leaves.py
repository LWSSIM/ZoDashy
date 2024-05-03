#!/usr/bin/env python3
""" API for Leave CRUD """


from backend.models import storage
from backend.models.employee import Employee
from backend.models.leave import Leave
from backend.api.v1.views import app_views
from flask import jsonify, request, abort
from sqlalchemy.exc import IntegrityError
from datetime import datetime


@app_views.get('/employees/<employee_id>/leaves')
def get_employee_leaves(employee_id):
    """ get leaves by employee_id """
    employee = storage.get(Employee, employee_id)
    if not employee:
        abort(404)

    return jsonify(
        [leave.to_dict() for leave in employee.leave]
    )


@app_views.get('/leaves/<leave_id>')
def get_leave(leave_id):
    """ get leave by id """
    leave = storage.get(Leave, leave_id)
    if not leave:
        abort(404)

    return jsonify(leave.to_dict())


@app_views.post('/employees/<employee_id>/leaves')
def create_leave(employee_id):
    """ create leave for employee """
    employee = storage.get(Employee, employee_id)
    if not employee:
        abort(404)

    data = request.get_json(force=True)
    if not data:
        abort(400, 'Invalid JSON')

    ensure = ['start_date', 'end_date', 'leave_type']
    for i in ensure:
        if i not in data:
            abort(400, f'Missing ({i})')
    try:
        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(data['end_date'], '%Y-%m-%d')
    except ValueError:
        abort(400, 'Invalid date format')
    if start_date < datetime.now():
        abort(400, 'Start date cannot be in the past')
    if start_date > end_date:
        abort(400, 'Start date cannot be after end date')

    data['employee_id'] = employee.id
    new_leave = Leave(**data)

    try:
        new_leave.save()
    except IntegrityError:
        abort(400, 'Invalid data')

    return jsonify(new_leave.to_dict()), 201


@app_views.put('/leaves/<leave_id>')
def update_leave(leave_id):
    """ update leave by id """
    leave = storage.get(Leave, leave_id)
    if not leave:
        abort(404)

    data = request.get_json(force=True)
    if not data:
        abort(400, 'Invalid data')

    for key, value in data.items():
        if key not in [
            'start_date', 'end_date',
            'leave_type', 'description', 'status'
        ]:
            abort(400, f'Invalid key ({key})')

    if 'start_date' in data:
        try:
            start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
        except ValueError:
            abort(400, 'Invalid start date format')
        if start_date > leave.end_date:
            abort(400, 'Start date cannot be after end date')

    if 'end_date' in data:
        try:
            end_date = datetime.strptime(data['end_date'], '%Y-%m-%d')
        except ValueError:
            abort(400, 'Invalid end date format')
        if leave.start_date > end_date:
            abort(400, 'End date cannot be before start date')

    if 'status' in data and data['status'] not in [
        'pending', 'approved', 'rejected'
    ]:
        abort(400, 'Invalid status, must be: (pending, approved or rejected)')

    for key, value in data.items():
        setattr(leave, key, value)

    try:
        leave.save()
    except IntegrityError:
        abort(400, 'Invalid data')

    return jsonify(leave.to_dict())


@app_views.delete('/leaves/<leave_id>')
def delete_leave(leave_id):
    """ delete leave by id """
    leave = storage.get(Leave, leave_id)
    if not leave:
        abort(404)

    leave.delete()
    storage.save()

    return jsonify({})
