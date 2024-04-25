#!/usr/bin/env python3
"""  Test Company Module:"""

import unittest
from backend.models.user import User
from backend.models.company import Company
from backend.models.department import Department
from backend.models import storage
from hashlib import sha256


user1 = {"firstName": "John",
         "lastName":
         "Doe", "email":
         "John@doe.com",
         "password": "doe123"}

company1 = {"name": "Company1",
            "description":
            "Company1 description"}


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

        user = User(**user1)
        company = Company(**company1)
        company.creator_id = user.id

        storage.new(user)
        storage.new(company)
        storage.save()

        q_user = storage.get(User, user.id)
        q_company = storage.get(Company, company.id)

        self.assertEqual(q_user, user)
        self.assertEqual(q_company, company)
        self.assertEqual(q_company.creator_id, user.id)
        user.delete()
        company.delete()
        storage.save()

    def test_company_department(self):
        """ test company department relationship """

        storage.reload()
        user = User(**user1)
        company = Company(**company1)
        company.creator_id = user.id
        department = Department(name="Department1", company_id=company.id)
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
        user.delete()
        company.delete()
        department.delete()
        storage.save()

    def test_correct_key_value(self):
        """ test correct key value pairs """

        storage.reload()

        user = User(**user1)
        company = Company(**company1)
        company.creator_id = user.id
        department = Department(name="Department1", company_id=company.id)
        storage.new(user)
        storage.new(company)
        storage.new(department)
        storage.save()

        q_user = storage.get(User, user.id)
        q_company = storage.get(Company, company.id)
        q_department = storage.get(Department, department.id)
        self.assertEqual(q_user.firstName, user1["firstName"])
        self.assertEqual(q_user.lastName, user1["lastName"])
        self.assertEqual(q_user.email, user1["email"])
        hash_pass = user1["password"]
        hash_pass = sha256(hash_pass.encode()).hexdigest()
        # test password is hashed
        self.assertEqual(q_user.password, hash_pass)
        self.assertEqual(q_company.name, company1["name"])
        self.assertEqual(q_company.description, company1["description"])
        self.assertEqual(q_department.name, "Department1")
        self.assertEqual(q_department.company_id, company.id)

        user.delete()
        company.delete()
        department.delete()
        storage.save()
