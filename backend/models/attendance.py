#!/usr/bin/env python3
""" Attendance class, to track employee's
    This is meant to happen daily, to be relevant
"""


from backend.models.base_model import BaseModel, Base
from sqlalchemy import Column, Date, String, Time, ForeignKey
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship
import datetime


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

    __table_args__ = (UniqueConstraint('date'), )

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def to_dict(self) -> dict:
        new = super().to_dict()

        if isinstance(self.date, datetime.date):
            new.update({'date': self.date.isoformat()})
        if isinstance(self.check_in, datetime.time):
            new.update({'check_in': self.check_in.isoformat()})
        if isinstance(self.check_out, datetime.time):
            new.update({'check_out': self.check_out.isoformat()})
        return new
