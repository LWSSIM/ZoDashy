#!/usr/bin/env python3
""" Test BaseModel Module:"""


import unittest
from models.base_model import BaseModel
from models.user import User
from models import storage

# Note: BaseModel is an __abstract__ class,
#         so it can't be stored directly in the database
#
# These tests are meant to be run with env vars, see example below:
#
# `$ POSTGRES_USER=postrgres POSTGRES_PASSWORD=postgres
#       POSTGRES_HOST=localhost POSTGRES_DB=postgres
#           python3 -m unittest discover tests`


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
        user = User(
            **{
                'lastName': 'sooma',
                'firstName': 'gooma',
                'password': 'poolapo',
                'manager': True,
                'email': 'poiula@poolai.com'
            }
        )
        user.save()
        self.assertEqual(storage.count(User), count + 1)
        user.delete()

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
            'lastName': 'sooma',
            'firstName': 'gooma',
            'password': 'poolapo',
            'manager': True,
            'email': 'poiula@poolai.com'
        }

        user = User(**user_dict)
        self.assertEqual(user.lastName, 'sooma')
        self.assertEqual(user.firstName, 'gooma')
        self.assertTrue(user.manager)
        self.assertEqual(user.email, 'poiula@poolai.com')
        # password should not be in the dict for security reasons
        self.assertTrue("password" not in user.to_dict())

    def test_user_save_and_delete(self):
        """ test user save """
        user_dict = {
            'lastName': 'sooma',
            'firstName': 'gooma',
            'password': 'poolapo',
            'manager': True,
            'email': 'poiula@poolai.com'
        }

        user = User(**user_dict)
        user.save()
        self.assertTrue(user.updated_at != user.created_at)
        user.delete()