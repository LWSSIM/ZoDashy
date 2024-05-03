#!/usr/bin/env python3
""" Leave class model """


from backend.models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Date, ForeignKey
from sqlalchemy.orm import relationship
import datetime


class Leave(BaseModel, Base):
    """ Allocate a specific number of leaves
    of a particular type to an Employee.
    """
    __tablename__ = 'leaves'

    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(String(10), default='pending', nullable=False)
    leave_type = Column(String(50), nullable=False)
    description = Column(String(256), nullable=True)
    employee_id = Column(String(60),
                         ForeignKey('employees.id'),
                         nullable=False)

    employee = relationship('Employee', backref='leave')

    def __init__(self, **kwargs) -> None:
        """ Initialize the Leave instance """
        super().__init__(**kwargs)

    def to_dict(self) -> dict:
        """ Return a dictionary representation of the Leave instance
                need to convert the dates to isoformat
        """
        new_dict = super().to_dict()

        if isinstance(self.start_date, datetime.date):
            new_dict.update({'start_date': self.start_date.isoformat()})
        if isinstance(self.end_date, datetime.date):
            new_dict.update({'end_date': self.end_date.isoformat()})

        return new_dict
