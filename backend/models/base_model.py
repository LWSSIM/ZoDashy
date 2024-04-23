#!/usr/bin/env python3
""" Base Model Module:
        Contains the BaseModel class that defines all common attributes/methods
"""

from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

format = "%Y-%m-%dT%H:%M:%S.%f"


class BaseModel(Base):
    """ BaseModel Class:
            Attributes:
                id (str): unique id for each instance
                created_at (datetime): time instance was created
                updated_at (datetime): time instance was updated
            methods:
                __init__: initializes instance of BaseModel
                __str__: returns string representation of instance
                save: updates instance with current datetime
                to_dict: returns dictionary representation of instance
    """

    __abstract__ = True

    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now)

    def __init__(self, *args, **kwargs):
        """ Init attrs """

        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if kwargs.get("created_at", None) and type(self.created_at) is str:
                self.created_at = datetime.strptime(
                    kwargs["created_at"], format
                )
            else:
                self.created_at = datetime.now()
            if kwargs.get("updated_at", None) and type(self.updated_at) is str:
                self.updated_at = datetime.strptime(
                    kwargs["updated_at"], format
                )
            else:
                self.updated_at = datetime.now()
            if kwargs.get("id", None) is None:
                self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at

    def __str__(self):
        """ Return string representation of instance """
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def to_dict(self):
        """ Return dictionary representation of instance """
        new_dict = self.__dict__.copy()
        if '_sa_instance_state' in new_dict:
            new_dict.pop('_sa_instance_state', None)
        new_dict['created_at'] = self.created_at.isoformat()
        new_dict['updated_at'] = self.updated_at.isoformat()
        new_dict['__class__'] = self.__class__.__name__
        if 'password' in new_dict:
            new_dict.pop('password', None)
        return new_dict

    def save(self):
        """ Update instance + time stamp """
        self.updated_at = datetime.now()
        from backend.models import storage
        storage.new(self)
        storage.save()

    def delete(self):
        """ Delete instance """
        from backend.models import storage
        storage.delete(self)
        storage.save()
