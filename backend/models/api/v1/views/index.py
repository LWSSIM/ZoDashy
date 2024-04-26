#!/usr/bin/env python3
""" index for api status/stats """


from flask import jsonify
from backend.models.api.v1.views import app_views
from backend.models import storage
from backend.models.user import User
from backend.models.company import Company
from backend.models.department import Department
from backend.models.employee import Employee
from backend.models.attendance import Attendance
from backend.models.leave import Leave
from backend.models.performance import Performance
from backend.models.documents import Document


@app_views.route('/status', methods=['GET'])
def status():
    """ status """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def stats():
    """ stats """

    cls = [
        User, Company, Department,
        Employee, Attendance, Leave,
        Performance, Document
    ]
    names = [
        "users", "companies", "departments",
        "employees", "attendace", "leaves",
        "performance", "documents"
    ]

    stats = {}
    for i in range(len(cls)):
        stats[names[i]] = storage.count(cls[i])
    return jsonify(stats)
