# coding=utf-8
"""Define table and operations for search records."""
import datetime
from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, DATE
from . import Base, session, handle_db_exception


class SearchRecords(Base):
    """Table constructed for search records."""
    __tablename__ = 'SearchRecords'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    brand_name = Column(VARCHAR(128), ForeignKey('Brands.name'))
    date = Column(DATE, nullable=False)


def add_record(_brand_name):
    """Add a search record to database."""
    record = SearchRecords()
    record.brand_name = _brand_name
    record.date = datetime.date.today()
    try:
        session.add(record)
        session.commit()
    except Exception as err:
        handle_db_exception(err)
