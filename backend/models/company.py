#!/usr/bin/env python3
""" Company module,
    this class is be the root of the company structure
"""


from backend.models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Company(BaseModel, Base):
    """ Comany class:
        Users have to create this object first,
        all other models wld be linked to this one
        as their parent either directly on through other objects
    """

    __tablename__ = "companies"

    name = Column(String(128), nullable=False)
    description = Column(String(255))
    creator_id = Column(String(60), ForeignKey('users.id'))

    creator = relationship("User", back_populates="companies")
    departments = relationship(
        "Department",
        back_populates="company",
        cascade="all, delete-orphan",
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
