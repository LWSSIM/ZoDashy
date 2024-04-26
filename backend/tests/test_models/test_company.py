#!/usr/bin/env python3
"""  Test Company Module:"""

import unittest
from backend.models.user import User
from backend.models.company import Company
from backend.models.department import Department
from backend.models import storage
from hashlib import sha256
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


class TestCompany(unittest.TestCase):
    """ Test Company Class """
    def setUp(self):
        """ Setup """
        storage.reload()

    def tearDown(self):
        storage.close()

    def test_is_instance(self):
        """ Instance """
        company = Company()
        self.assertIsInstance(company, Company)

    def test_get_company(self):
        """ get company """
        companies = storage.all(Company)
        if not companies:
            print("No companies in storage")
            return
        for company in companies.values():
            self.assertEqual(company, storage.get(Company, company.id))

    def test_company_user(self):
        """ test company user """
        storage.reload()

        user = fake_user()
        company = fake_company()
        company.creator_id = user.id

        storage.new(user)
        storage.new(company)
        storage.save()

        q_user = storage.get(User, user.id)
        q_company = storage.get(Company, company.id)

        self.assertEqual(q_user, user)
        self.assertEqual(q_company, company)
        self.assertEqual(q_company.creator_id, user.id)
        self.assertEqual(q_user.companies[0], company)

    def test_company_department(self):
        """ test company department relationship """

        storage.reload()
        user = fake_user()
        company = fake_company()

        company.creator_id = user.id
        department = Department(name="Department of things", company_id=company.id)

        storage.new(user)
        storage.new(company)
        storage.new(department)
        storage.save()
        self.assertIsNotNone(company.departments)
        self.assertIsInstance(department, Department)
        q_company = storage.get(Company, company.id)
        q_department = storage.get(Department, department.id)
        self.assertEqual(q_company, company)
        self.assertEqual(q_department, department)
        self.assertEqual(q_department.company_id, company.id)

    def test_correct_key_value(self):
        """ test correct key value pairs """

        storage.reload()

        user = fake_user()
        company = fake_company()
        company.creator_id = user.id
        department = Department(name="Department1", company_id=company.id)
        storage.new(user)
        storage.new(company)
        storage.new(department)
        storage.save()

        q_user = storage.get(User, user.id)
        q_company = storage.get(Company, company.id)
        q_department = storage.get(Department, department.id)
        self.assertEqual(q_user.userName, user.userName)
        self.assertEqual(q_user.name, user.name)
        self.assertEqual(q_user.email, user.email)


        # test password is hashed
        self.assertEqual(q_user.password, user.password)
        self.assertEqual(q_company.name, company.name)
        self.assertEqual(q_company.description, company.description)
        self.assertEqual(q_department.name, "Department1")
        self.assertEqual(q_department.company_id, company.id)
