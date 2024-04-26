#!/usr/bin/env python3
""" Test Employee Module:"""


import unittest
from backend.models.user import User
from backend.models.company import Company
from backend.models.department import Department
from backend.models.employee import Employee
from backend.models import storage
from faker import Faker


def fake_user():
    """ fake model """
    fake = Faker()
    return User(
        userName=fake.user_name(),
        email=fake.email(),
        password=fake.password(),
        name=fake.name(),
    )
def fake_company():
    """ fake model """
    fake = Faker()
    return Company(
        name=fake.company(),
        description=fake.text(),
    )
def fake_department():
    """ fake model """
    fake = Faker()
    return Department(
        name=fake.company(),
        description=fake.text(),
    )
def fake_employee():
    """ fake model """
    fake = Faker()
    return Employee(
        firstName=fake.first_name(),
        lastName=fake.last_name(),
        email=fake.email(),
        phone=fake.phone_number()[:20],
        jobTitle=fake.job(),
    )


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

        user = fake_user()
        company = fake_company()
        department = fake_department()
        employee = fake_employee()

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
