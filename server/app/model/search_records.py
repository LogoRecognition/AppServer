# coding=utf-8
"""Define table and operations for search records."""
import datetime
from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, DATE, func
from . import Base, session, handle_db_exception, brands


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


def get_heat_brands(num):
    try:
        brand_names = session.query(SearchRecords.brand_name, func.count(SearchRecords.brand_name))\
            .group_by(SearchRecords.brand_name).all()
        brand_names = sorted(brand_names, key=lambda x: x[1], reverse=True)
        if num:
            brand_names = brand_names[:num]
        brand_names = [x[0] for x in brand_names]
        result = brands.find_brands_by_name_list(brand_names)
        session.commit()
        return result
    except Exception as err:
        handle_db_exception(err)
