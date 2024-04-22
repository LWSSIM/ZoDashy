#!/usr/bin/env python3
""" User Module:
        Contains the User class that defines all common attributes/methods
"""


from models.base_model import BaseModel, Base
from hashlib import sha256
from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """ User Class: Different from employee
        Attributes:
            email (str): user email
            password (str): user password
            ...
    """

    __tablename__ = 'users'
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    firstName = Column(String(128), nullable=False)
    lastName = Column(String(128), nullable=False)
    manager = Column(Boolean, default=False)
#    Department_id = relationship("Department", back_ref="users")
#    Employee_id = relationship("Employee", back_ref="users")

    def __init__(self, *args, **kwargs):
        """ Init attrs """
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """ Set password as hash """
        if name == "password":
            value = sha256(value.encode()).hexdigest()
        super().__setattr__(name, value)