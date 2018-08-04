# coding=utf-8
"""Define table and operations for collections."""
from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, UniqueConstraint, and_
from . import Base, session, handle_db_exception


class Collections(Base):
    """Table constructed for collections."""
    __tablename__ = 'Collections'

    collection_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = Column(Integer, ForeignKey('Users.user_id'))
    brand_name = Column(VARCHAR(128), ForeignKey('Brands.name'))
    UniqueConstraint(user_id, brand_name)


def add_collection(user_id, brand_name):
    try:
        collection = Collections()
        collection.user_id = user_id
        collection.brand_name = brand_name
        session.add(collection)
        session.commit()
    except Exception as err:
        handle_db_exception(err)


def delete_collection(user_id, brand_name):
    try:
        result = session.query(Collections)\
            .filter(and_(Collections.user_id == user_id), Collections.brand_name == brand_name)\
            .delete()
        session.commit()
        return result
    except Exception as err:
        handle_db_exception(err)


def get_collections_by_user(user_id):
    """Get a list of brand names collected by the user."""
    try:
        result = session.query(Collections.brand_name) \
            .filter(Collections.user_id == user_id) \
            .all()
        result = [x for x, in result]
        session.commit()
        return result
    except Exception as err:
        handle_db_exception(err)
