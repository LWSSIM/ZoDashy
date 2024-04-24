#!/usr/bin/env python3
""" Leave class model """


from backend.models.base_model import BaseModel, Base
from sqlalchemy import Column, Boolean, String, Date, ForeignKey
from sqlalchemy.orm import relationship


class Leave(BaseModel, Base):
    """ Allocate a specific number of leaves
    of a particular type to an Employee.
    """
    __tablename__ = 'leaves'

    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(Boolean, default=False)
    leave_type = Column(String(50), nullable=False)
    description = Column(String(256), nullable=True)
    employee_id = Column(String(60),
                         ForeignKey('employees.id'),
                         nullable=False)

    employee = relationship('Employee', backref='leave')

    def __init__(self, **kwargs) -> None:
        """ Initialize the Leave instance """
        super().__init__(**kwargs)
