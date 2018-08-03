# coding=utf-8
"""Define table and operations for search records."""
from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, DATE
from . import Base, session, handle_db_exception


class SearchRecords(Base):
    """Table constructed for search records."""
    __tablename__ = 'SearchRecords'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    brand_name = Column(VARCHAR(128), ForeignKey('Brands.name'))
    date = Column(DATE, nullable=False)
