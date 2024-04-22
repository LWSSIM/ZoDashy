#!/usr/bin/env python3
""" DB Module:
        Contains the DB class that defines the database connection
"""


from models.user import User
from models.base_model import Base
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


db_user = getenv("POSTGRES_USER")
password = getenv("POSTGRES_PASSWORD")
host = getenv("POSTGRES_HOST")
database = getenv("POSTGRES_DB")

database_url = f"postgresql://{db_user}:{password}@{host}/{database}"

classes = {
     "User": User,
}
#    "Department": Department,
#    "Employee": Employee,
#    "Attendance": Attendance,
#    "Leave": Leave,
#    "Progress": Progress,
#    "Document": Document,


class DB:
    """ Database connection + orm
            Note:
                using POSTGRESQL, can be changed to anything that supports orm
    """

    __engine = None
    __session = None

    def __init__(self) -> None:
        """ Init DB engine """
        self.__engine = create_engine(database_url, pool_pre_ping=True)

    # ORM methods
    def all(self, cls=None):
        """ Return all instances of a class """
        instances = {}
        if cls:
            objs = self.__session().query(cls).all()
            for obj in objs:
                key = obj.__class__.__name__ + '.' + obj.id
                instances[key] = obj
        else:
            for _, value in classes.items():
                objs = self.__session().query(value).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    instances[key] = obj
        return instances

    def get(self, cls, id):
        """ Return an instance of a class """
        if cls and id:
            key = cls.__name__ + '.' + id
            return self.all(cls).get(key)
        return None

    def count(self, cls=None):
        """ Return the number of instances of a class """
        return len(self.all(cls))

    # Session management
    def reload(self):
        """ Reload the database """
        Base.metadata.create_all(self.__engine)

        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False
        )
        Session = scoped_session(session_factory)
        self.__session = Session

    def save(self):
        """ Commit all changes of the current session """
        self.__session.commit()

    def close(self):
        """ Close the database """
        self.__session.remove()

    def new(self, obj):
        """ Add an instance to the session """
        self.__session.add(obj)

    def delete(self, obj=None):
        """ Delete an instance from the session """
        if obj:
            self.__session.delete(obj)
