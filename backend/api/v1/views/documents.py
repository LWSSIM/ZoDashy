#!/usr/bin/env python3
""" Document API endpoints """


from backend.models import storage
from backend.models.department import Department
from backend.models.document import Document
from backend.api.v1.views import app_views
from flask import jsonify, request, abort
from sqlalchemy.exc import IntegrityError


@app_views.get('/departments/<department_id>/documents')
def get_department_documents(department_id):
    """ Retrieve all documents for a department """
    department = storage.get(Department, department_id)
    if department is None:
        abort(404)

    documents = [
        document.to_dict() for document in department.documents
    ]
    return jsonify(documents)


@app_views.get('/documents/<document_id>')
def get_document(document_id):
    """ Retrieve a document """
    document = storage.get(Document, document_id)
    if document is None:
        abort(404)

    return jsonify(document.to_dict())


@app_views.post('/departments/<department_id>/documents')
def create_document(department_id):
    """ Create a new document """
    department = storage.get(Department, department_id)
    if department is None:
        abort(404)

    data = request.get_json(force=True)
    if data is None:
        abort(400, 'Not a JSON')
    if 'title' not in data:
        abort(400, 'Missing title')
    if 'content' not in data:
        abort(400, 'Missing content')

    data['department_id'] = department_id
    document = Document(**data)

    try:
        document.save()
    except IntegrityError:
        abort(400, 'Invalid data')

    return jsonify(document.to_dict()), 201


@app_views.put('/documents/<document_id>')
def update_document(document_id):
    """ Update a document """
    document = storage.get(Document, document_id)
    if document is None:
        abort(404)

    data = request.get_json(force=True)
    if data is None:
        abort(400, 'Not a JSON')

    for key, value in data.items():
        if key not in ['title', 'description', 'content']:
            abort(400, f'Invalid key {key}')

        setattr(document, key, value)

    try:
        document.save()
    except IntegrityError:
        abort(400, 'Invalid data')

    return jsonify(document.to_dict())


@app_views.delete('/documents/<document_id>')
def delete_document(document_id):
    """ Delete a document """
    document = storage.get(Document, document_id)
    if document is None:
        abort(404)

    document.delete()
    storage.save()

    return jsonify({})
