#!/usr/bin/env python3
""" Document class model """


from backend.models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.types import LargeBinary
from sqlalchemy.orm import relationship


class Document(BaseModel, Base):
    """ Department will have a list of its documents """
    __tablename__ = 'documents'

    title = Column(String(256), nullable=False)
    description = Column(String(256), nullable=True)
    content = Column(LargeBinary, nullable=False)
    department_id = Column(String(60),
                           ForeignKey('departments.id'),
                           nullable=False)

    department = relationship('Department', backref='documents')

    def __init__(self, **kwargs) -> None:
        """ Initialize the Document instance """
        super().__init__(**kwargs)
