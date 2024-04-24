#!/usr/bin/env python3
""" Attendance class, to track employee's
    This is meant to happen daily, to be relevant
"""


from backend.models.base_model import BaseModel, Base
from sqlalchemy import Column, Date, String, Time, ForeignKey
from sqlalchemy.orm import relationship


class Attendance(BaseModel, Base):
    """ record stating whether an Employee was present on a particular. """

    __tablename__ = 'attendances'
    date = Column(Date, nullable=False)
    check_in = Column(Time, nullable=False)
    check_out = Column(Time, nullable=False)
    employee_id = Column(String(60),
                         ForeignKey('employees.id'),
                         nullable=False)

    employee = relationship("Employee", backref="attendance")

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
