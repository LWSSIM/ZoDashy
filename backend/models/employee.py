#!/usr/bin/env python3
""" Employee Class """


from backend.models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Employee(BaseModel, Base):
    """ This will Be The Core model of each department
        all further models will be be linked to it aswell,
        ensuring the bl of tracking each Employee.
    """

    __tablename__ = "employees"

    firstName = Column(String(128), nullable=False)
    lastName = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)
    phone = Column(String(20))
    jobTitle = Column(String(128), nullable=False)
    department_id = Column(String(60),
                           ForeignKey('departments.id'),
                           nullable=False)

    department = relationship("Department", back_populates="employees")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
