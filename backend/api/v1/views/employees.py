#!/usr/bin/env python3
""" API for employee CRUD """


from backend.models.company import Company
from backend.models.department import Department
from backend.models.employee import Employee
from backend.models import storage
from backend.api.v1.views import app_views
from sqlalchemy.exc import IntegrityError
from flask import request, abort, jsonify


@app_views.route('/departments/<department_id>/employees', methods=['GET'])
def get_dep_employees(department_id):
    """ get all employees by dep id """
    department = storage.get(Department, department_id)
    if not department:
        abort(404)

    return jsonify([employee.to_dict() for employee in department.employees])


@app_views.get('/companies/<company_id>/employees')
def get_comp_employees(company_id):
    """ get all employees by company  id """
    company = storage.get(Company, company_id)
    if not company:
        abort(404)

    result = []
    for d in company.departments:
        for e in d.employees:
            result.append(e.to_dict())

    return jsonify(result)


@app_views.get('/employees/<employee_id>')
def get_employee(employee_id):
    """ get an emp by id """
    employee = storage.get(Employee, employee_id)
    if not employee:
        abort(404)

    return jsonify(employee.to_dict())


@app_views.post('/departments/<department_id>/employees')
def create_employee(department_id):
    """ create new employee """
    department = storage.get(Department, department_id)
    if not department:
        abort(404)

    data = request.get_json(force=True)
    if not data:
        abort(400, 'Not a valid JSON')

    ensure = ['firstName', 'lastName', 'email', 'jobTitle']
    for i in ensure:
        if i not in data or data[i] == '':
            abort(400, f"Missing ({i})")

    data['department_id'] = department.id
    employee = Employee(**data)
    emps = storage.all(Employee)
    for e in emps.values():
        if e.email == employee.email:
            abort(400, 'Email already exists')

    try:
        employee.save()
    except IntegrityError as e:
        abort(400, str(e))
    finally:
        return jsonify(employee.to_dict()), 201


@app_views.delete('/employees/<employee_id>')
def delete_employee(employee_id):
    """ delete amployee by id """
    employee = storage.get(Employee, employee_id)
    if not employee:
        abort(404)

    try:
        employee.delete()
    except IntegrityError as e:
        abort(400, str(e))
    finally:
        return jsonify({})


@app_views.put('/employees/<employee_id>')
def update_employee(employee_id):
    """ update employee attrs by id """
    employee = storage.get(Employee, employee_id)
    if not employee:
        abort(404)

    data = request.get_json(force=True)
    if not data:
        abort(400, 'Not a valid JSON')

    ensure = ['firstName', 'lastName', 'phone', 'email', 'jobTitle']

    for k, v in data.items():
        if k not in ensure:
            abort(400, f'Invalid key ({k})')
        setattr(employee, k, v)

    try:
        employee.save()
    except IntegrityError as e:
        abort(400, str(e))
    finally:
        return jsonify(employee.to_dict())
