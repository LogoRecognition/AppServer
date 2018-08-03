# coding=utf-8
"""Initialize database connection."""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
session = None


def init_db(_user,
            _password,
            _db_name):
    """Initialize database connections and create tables."""

    global session
    db_engine = create_engine(
        'mysql+pymysql://{}:{}@localhost/{}?charset=utf8'.format(
            _user, _password, _db_name),
        echo=True)
    session = sessionmaker(bind=db_engine)()

    # Create all tables
    from . import brands, classic_goods, search_records
    Base.metadata.create_all(db_engine)


def handle_db_exception(ex):
    """Roll back session and raise the exception."""
    session.rollback()
    raise ex
