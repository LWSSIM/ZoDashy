#!/usr/bin/env python3
""" Test BaseModel Module:"""


import unittest
from backend.models.base_model import BaseModel
from backend.models.user import User
from backend.models import storage
from faker import Faker

# Note: BaseModel is an __abstract__ class,
#         so it can't be stored directly in the database

# These tests are meant to be run with env vars, see example below:
#
# `$ POSTGRES_USER=postrgres POSTGRES_PASSWORD=postgres
#       POSTGRES_HOST=localhost POSTGRES_DB=postgres
#           python3 -m unittest discover tests`


def fake_user():
    """ fake model """
    fake = Faker()
    return User(
        userName=fake.user_name(),
        email=fake.email(),
        password=fake.password(),
        name=fake.name(),
    )


class TestMainFunction(unittest.TestCase):
    """ Test BaseModel Class """

    def setUp(self):
        """ Setup """
        storage.reload()

    def tearDown(self):
        storage.close()

    def test_is_instance(self):
        """ Instance """
        base = BaseModel()
        user = User()
        self.assertIsInstance(base, BaseModel)
        self.assertIsInstance(user, User)

    def test_storage_all(self):
        """ shld return DICT """
        objs = storage.all()
        self.assertIs(type(objs), dict)

    def test_get_user(self):
        """ get user """
        users = storage.all(User)
        if not users:
            print("No users in storage")
            return
        for user in users.values():
            self.assertEqual(user, storage.get(User, user.id))

    def test_count(self):
        """ count """
        count = storage.count()
        self.assertTrue(count >= 0)
        count = storage.count(User)
        self.assertTrue(count >= 0)
        user = fake_user()
        user.save()
        self.assertEqual(storage.count(User), count + 1)

    def test_basemodel_inheritance(self):
        """ does a model get parent attrs correctly """
        new_user = User()
        self.assertIsNotNone(new_user)
        self.assertTrue(new_user.updated_at == new_user.created_at)
        self.assertTrue(new_user.id in new_user.to_dict().values())
        self.assertTrue("created_at" in new_user.to_dict())
        self.assertTrue("updated_at" in new_user.to_dict())

    def test_user_kwargs(self):
        """ test user with kwargs """
        user_dict = {
            'userName': 'sooma',
            'name': 'gooma',
            'password': 'poolapo',
            'manager': True,
            'email': 'poiula@poolai.com'
        }

        user = User(**user_dict)
        self.assertEqual(user.userName, 'sooma')
        self.assertEqual(user.name, 'gooma')
        self.assertTrue(user.manager)
        self.assertEqual(user.email, 'poiula@poolai.com')
        # password should not be in the dict for security reasons
        self.assertTrue("password" not in user.to_dict())

    def test_user_save_and_delete(self):
        """ test user save """
        user = fake_user()
        count = storage.count(User)
        user.save()
        self.assertEqual(storage.count(User), count + 1)
        self.assertTrue(user.updated_at != user.created_at)
        self.assertEqual(storage.get(User, user.id), user)
        user.delete()
        self.assertEqual(storage.count(User), count)
        self.assertIsNone(storage.get(User, user.id))
