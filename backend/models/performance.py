#!/usr/bin/env python3
""" Performance class model """


from backend.models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.types import DECIMAL
from sqlalchemy.orm import relationship


class Performance(BaseModel, Base):
    """ Performance class model """
    __tablename__ = 'performances'

    review = Column(String(256), nullable=True)
    score = Column(DECIMAL(5, 2), nullable=False)
    employee_id = Column(String(60),
                         ForeignKey('employees.id'),
                         nullable=False)

    employee = relationship('Employee', backref='performance')

    def __init__(self, **kwargs) -> None:
        """ Initialize the Performance instance """
        super().__init__(**kwargs)
