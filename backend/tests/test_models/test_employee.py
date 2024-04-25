#!/usr/bin/env python3
""" Test Employee Module:"""


import unittest
from backend.models.user import User
from backend.models.company import Company
from backend.models.department import Department
from backend.models.employee import Employee
from backend.models import storage


user1 = {"firstName": "John",
         "lastName": "Doe",
         "email": "John@doe.com",
         "password": "doe123",
         "manager": True}
company1 = {"name": "Company1",
            "description": "Company1 description"}
department1 = {"name": "Department1",
               "description": "Department1 description"}
employee1 = {"firstName": "John",
             "lastName": "Doe",
             "email": "John@doe.com",
             "phone": "1234567890",
             "jobTitle": "CEO of things"}


class TestEmployee(unittest.TestCase):
    """ Test Employee Class """

    def setUp(self):
        """ Setup """
        storage.reload()

    def tearDown(self):
        storage.close()

    def test_is_instance(self):
        """ Instance """
        employee = Employee()
        self.assertIsInstance(employee, Employee)

    def test_get_employee(self):
        """ get employee """
        employees = storage.all(Employee)
        if not employees:
            print("No employees in storage")
            return
        for employee in employees.values():
            self.assertEqual(employee, storage.get(Employee, employee.id))

    def test_employee_user(self):
        """ test employee user
            and also get + delete + save
            + relationships
        """
        storage.reload()

        user = User(**user1)
        company = Company(**company1)
        department = Department(**department1)
        employee = Employee(**employee1)

        company.creator_id = user.id
        department.company_id = company.id
        employee.department_id = department.id

        storage.new(user)
        storage.new(company)
        storage.new(department)
        storage.new(employee)
        storage.save()

        self.assertEqual(storage.get(User, user.id), user)
        self.assertEqual(storage.get(Company, company.id), company)
        self.assertEqual(storage.get(Department, department.id), department)
        self.assertEqual(storage.get(Employee, employee.id), employee)
        self.assertEqual(storage.get(Company, company.id).creator_id, user.id)
        self.assertEqual(storage.get(Department, department.id).company_id,
                         company.id)
        self.assertEqual(storage.get(Employee, employee.id).department_id,
                         department.id)
        storage.delete(user)
        storage.delete(company)
        storage.delete(department)
        storage.delete(employee)
        storage.save()
