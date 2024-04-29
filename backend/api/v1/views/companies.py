#!/usr/bin/env python3
""" API For companies crud """


from backend.models import storage
from backend.models.user import User
from backend.models.company import Company
from backend.api.v1.views import app_views
from flask import jsonify, request, abort
from sqlalchemy.exc import IntegrityError


@app_views.route('/companies', methods=['GET'])
def get_companies():
    """ get all companies in db """
    companies = storage.all(Company)
    return jsonify([company.to_dict() for company in companies.values()])


@app_views.route('/companies/<company_id>', methods=['GET'])
def get_company(company_id):
    """ get company by id """
    company = storage.get(Company, company_id)
    if company:
        return jsonify(company.to_dict())
    abort(404)


@app_views.route('/users/<user_id>/companies', methods=['GET'])
def get_user_companies(user_id):
    """ get all companies for a user """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify([company.to_dict() for company in user.companies])


@app_views.route('/user/<user_id>/companies', methods=['POST'])
def create_company(user_id):
    """ create company """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    data = request.get_json(force=True)
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data or data['name'] == '':
        abort(400, 'Missing name')

    data['creator_id'] = user_id
    company = Company(**data)
    companies = storage.all(Company)

    for c in companies.values():
        if c.name == company.name:
            abort(400, 'Company already exists')
    try:
        company.save()
    except IntegrityError as e:
        abort(400, str(e))
    finally:
        return jsonify(company.to_dict()), 201


@app_views.route('/companies/<company_id>', methods=['PUT'])
def update_company(company_id):
    """ update company by id """
    company = storage.get(Company, company_id)
    if not company:
        abort(404)
    data = request.get_json(force=True)
    if not data:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['name', 'description']:
            abort(400, 'Invalid key')
        setattr(company, key, value)
    try:
        company.save()
    except IntegrityError as e:
        abort(400, str(e))
    finally:
        return jsonify(company.to_dict())


@app_views.route('/companies/<company_id>', methods=['DELETE'])
def delete_company(company_id):
    """ delete company by id """
    company = storage.get(Company, company_id)
    if not company:
        abort(404)
    storage.delete(company)
    storage.save()
    return jsonify({}), 200
