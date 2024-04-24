#!/usr/bin/env python3
""" Document class model """


from backend.models.base_model import BaseModel, Base
from sqlalchemy import BLOB, Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Document(BaseModel, Base):
    """ Department will have a list of its documents """
    __tablename__ = 'documents'

    title = Column(String(256), nullable=False)
    description = Column(String(256), nullable=True)
    content = Column(BLOB, nullable=False)
    department_id = Column(String(60),
                           ForeignKey('departments.id'),
                           nullable=False)

    department = relationship('Department', backref='document')

    def __init__(self, **kwargs) -> None:
        """ Initialize the Document instance """
        super().__init__(**kwargs)
