#!/usr/bin/env python3
""" DB Module:
        Contains the DB class that defines the database connection
"""


from backend.models.base_model import Base
from backend.models.user import User
from backend.models.company import Company
from backend.models.department import Department
from backend.models.employee import Employee
from backend.models.documents import Document
from backend.models.leave import Leave
from backend.models.attendance import Attendance
from backend.models.performance import Performance

from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


db_user = getenv("POSTGRES_USER")
password = getenv("POSTGRES_PASSWORD")
host = getenv("POSTGRES_HOST")
database = getenv("POSTGRES_DB")
env_type = getenv("ENV_TYPE")

database_url = f"postgresql://{db_user}:{password}@{host}/{database}"

classes = {
    "User": User,
    "Company": Company,
    "Department": Department,
    "Employee": Employee,
    "Document": Document,
    "Leave": Leave,
    "Attendance": Attendance,
    "Performance": Performance,
}


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

        if env_type == "test_db":
            Base.metadata.drop_all(self.__engine)

    # ORM methods
    def all(self, cls=None) -> dict:
        """ Return all instances(objs) of a class(es) """
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

    def get(self, cls, id) -> object:
        """ Return an instance of a class """
        if cls and id:
            key = cls.__name__ + '.' + id
            return self.all(cls).get(key)
        return None

    def count(self, cls=None) -> int:
        """ Return the number of instances of a class """
        return len(self.all(cls))

    # Session management methods
    def reload(self) -> None:
        """ Reload the database with a new session """
        Base.metadata.create_all(self.__engine)

        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False
        )
        Session = scoped_session(session_factory)
        self.__session = Session

    def save(self) -> None:
        """ Commit all changes of the current session """
        try:
            self.__session.commit()
        except Exception:
            self.__session.rollback()
            raise

    def close(self) -> None:
        """ Close the database """
        self.__session.remove()

    def new(self, obj) -> None:
        """ Add an instance to the session """
        self.__session.add(obj)

    def delete(self, obj=None) -> None:
        """ Delete an instance from the session """
        if obj:
            self.__session.delete(obj)
