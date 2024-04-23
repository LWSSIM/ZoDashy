#!/usr/bin/env python3
""" Department Module:
        A department in a company or organization
"""


from backend.models.base_model import BaseModel, Base
from sqlalchemy import Column, ForeignKey, String, Text
from sqlalchemy.orm import relationship


class Department(BaseModel, Base):
    """ Class Department:
        Linked to a company, can't exist independently,
        it will also have a link to employees in it.

        Note:
            only a user shld be able to modify this,
            and subsequent objects!
            an employee can be elevated to a user, by the creator.
    """

    __tablename__ = "departments"

    name = Column(String(128), nullable=False)
    description = Column(String(255))
    company_id = Column(String(60), ForeignKey('companies.id'))
    manager_id = Column(String(60), ForeignKey('users.id'))

    company = relationship("Company", back_populates="departments")
