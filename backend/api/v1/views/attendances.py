#!/usr/bin/env python3
""" api for employee attendance CRUD """


from backend.models import storage
from backend.models.employee import Employee
from backend.models.attendance import Attendance
from backend.api.v1.views import app_views
from flask import request, abort, jsonify
from sqlalchemy.exc import IntegrityError
from datetime import datetime


@app_views.get('/employees/<employee_id>/attendances')
def get_employee_attendance(employee_id):
    """ get attendance by employee_id """
    employee = storage.get(Employee, employee_id)
    if not employee:
        abort(404)

    return jsonify([att.to_dict() for att in employee.attendance])


@app_views.get('/attendances/<attendance_id>')
def get_attendance(attendance_id):
    """ get attendance by id """
    attendance = storage.get(Attendance, attendance_id)
    if not attendance:
        abort(404)

    return jsonify(attendance.to_dict())


@app_views.post('/employees/<employee_id>/attendances')
def create_attendance(employee_id):
    """ create attendance for employee """
    employee = storage.get(Employee, employee_id)
    if not employee:
        abort(404)

    data = request.get_json(force=True)
    if not data:
        abort(400, 'Invalid JSON')

    ensure = ['date', 'check_in', 'check_out']
    for i in ensure:
        if i not in data:
            abort(400, f'Missing ({i})')

    try:
        check_date = datetime.strptime(data['date'], '%Y-%m-%d')
    except ValueError:
        abort(400, 'Invalid date format')
    if check_date > datetime.now():
        abort(400, 'Date cannot be in the future')

    check_date = (storage._DB__session
                  .query(Attendance)
                  .filter_by(date=data['date'])
                  .first())
    if check_date:
        abort(400, 'Date already exists')

    try:
        check_in = datetime.strptime(data['check_in'], '%H:%M')
    except ValueError:
        abort(400, 'Invalid Check in format')
    try:
        check_out = datetime.strptime(data['check_out'], '%H:%M')
    except ValueError:
        abort(400, 'Invalid Check out format')

    if check_in > check_out:
        abort(400, 'Check in cannot be after Check out')

    data['employee_id'] = employee.id
    attendance = Attendance(**data)

    try:
        attendance.save()
    except IntegrityError:
        abort(400, 'Invalid data')
    finally:
        return jsonify(attendance.to_dict()), 201


@app_views.delete('/attendances/<attendance_id>')
def delete_attendance(attendance_id):
    """ delete attendance by id """
    attendance = storage.get(Attendance, attendance_id)
    if not attendance:
        abort(404)

    attendance.delete()
    storage.save()

    return jsonify({})

#
# Don't think I need this now.
# maybe if I add more functionality for this model.
#


@app_views.put('/attendances/<attendance_id>')
def update_attendance(attendance_id):
    """ update attendance by id """
    attendance = storage.get(Attendance, attendance_id)
    if not attendance:
        abort(404)

    data = request.get_json(force=True)
    if not data:
        abort(400, 'Invalid JSON')

    check_in, check_out = None, None

    for key, value in data.items():
        if key not in ['date', 'check_in', 'check_out']:
            abort(400, f'Invalid key ({key})')

        if key == 'date':
            try:
                check_date = datetime.strptime(value, '%Y-%m-%d')
            except ValueError:
                abort(400, 'Invalid date format')

            check_date = (storage.__session
                          .query(Attendance)
                          .filter_by(date=value)
                          .first())
            if check_date:
                abort(400, 'Date already exists')

        if key == 'check_in':
            try:
                check_in = datetime.strptime(value, '%H:%M')
            except ValueError:
                abort(400, 'Invalid Check in format')

        if key == 'check_out':
            try:
                check_out = datetime.strptime(value, '%H:%M')
            except ValueError:
                abort(400, 'Invalid Check out format')

        if check_in and check_out and check_in > check_out:
            abort(400, 'Check in cannot be after Check out')

        if not (check_in and check_out):
            if check_in:
                if attendance.check_out < check_in.time():
                    abort(400, 'Check in cannot be after Check out')
            elif check_out:
                if attendance.check_in > check_out.time():
                    abort(400, 'Check in cannot be after Check out')

        setattr(attendance, key, value)

    try:
        attendance.save()
    except IntegrityError:
        abort(400, 'Invalid data')
    finally:
        return jsonify(attendance.to_dict())
