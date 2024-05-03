#!/usr/bin/env python3
""" API For departments crud """


from backend.models import storage
from backend.models.company import Company
from backend.models.department import Department
from backend.api.v1.views import app_views
from flask import jsonify, request, abort
from sqlalchemy.exc import IntegrityError


@app_views.route('/departments', methods=['GET'])
def get_departments():
    departments = storage.all(Department)
    if departments:
        return jsonify([dep.to_dict() for dep in departments.values()])


@app_views.route('/companies/<company_id>/departments', methods=['GET'])
def get_company_departments(company_id):
    """ get all deps in a company """
    company = storage.get(Company, company_id)

    if not company:
        abort(404)

    return jsonify(
        [department.to_dict() for department in company.departments]
    )


@app_views.route('/departments/<department_id>', methods=['GET'])
def get_department(department_id):
    """ get dep by id """
    department = storage.get(Department, department_id)
    if department:
        return jsonify(department.to_dict())
    abort(404)


@app_views.route('/companies/<company_id>/departments', methods=['POST'])
def create_department(company_id):
    """ create new dep in company """
    company = storage.get(Company, company_id)
    if not company:
        abort(404)
    data = request.get_json(force=True)

    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data or data['name'] == '':
        abort(400, 'Missing name')

    data['company_id'] = company_id
    department = Department(**data)
    deps = storage.all(Department)
    for d in deps.values():
        if d.name == department.name:
            abort(400, 'Department already exists')

    try:
        department.save()
    except IntegrityError:
        abort(400, 'Ivalid data')
    finally:
        return jsonify(department.to_dict()), 201


@app_views.route('/departments/<department_id>', methods=['PUT'])
def update_department(department_id):
    """ update dep by id """
    department = storage.get(Department, department_id)
    if not department:
        abort(404)
    data = request.get_json(force=True)
    if not data:
        abort(400, 'Not a JSON')

    for k, v in data.items():
        if k not in ['name', 'description']:
            abort(400, 'Invalid key')
        setattr(department, k, v)

    try:
        department.save()
    except IntegrityError:
        abort(400, 'Ivalid data')
    finally:
        return jsonify(department.to_dict())


@app_views.route('/departments/<department_id>', methods=['DELETE'])
def delete_department(department_id):
    """ delete dep by id """
    department = storage.get(Department, department_id)
    if not department:
        abort(404)

    department.delete()
    storage.save()
    return jsonify({})
