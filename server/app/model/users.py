# coding=utf-8
"""Define table and operations for users."""
from flask_login import UserMixin
from sqlalchemy import Column, Integer, VARCHAR, DATE, BOOLEAN, TEXT
from . import Base, session, handle_db_exception


class Users(Base, UserMixin):
    """Table constructed for users."""
    __tablename__ = 'Users'

    user_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    user_name = Column(VARCHAR(128), nullable=False, unique=True)
    password = Column(VARCHAR(256), nullable=False)
    email = Column(VARCHAR(128), nullable=False)
    birthday = Column(DATE, nullable=True)
    gender = Column(BOOLEAN, nullable=True)

    def to_json(self):
        """Return a json for the record."""
        return {
            'user_id': self.user_id,
            'user_name': self.user_name,
            'email': self.email,
            'birthday': str(self.birthday) if self.birthday else None,
            'gender': int(self.gender)
        }

    def get_id(self):
        """Override UserMixin.get_id()"""
        return self.user_id


def add_user(user_name, password, email, birthday, gender):
    try:
        user = Users()
        user.user_name = user_name
        user.password = password
        user.email = email
        user.birthday = birthday
        user.gender = gender
        session.add(user)
        session.commit()
        return user
    except Exception as err:
        handle_db_exception(err)


def find_user_by_id(user_id):
    try:
        user = session.query(Users).filter(Users.user_id == user_id).first()
        session.commit()
        return user
    except Exception as err:
        handle_db_exception(err)


def find_user_by_name(user_name):
    try:
        user = session.query(Users).filter(Users.user_name == user_name).first()
        session.commit()
        return user
    except Exception as err:
        handle_db_exception(err)