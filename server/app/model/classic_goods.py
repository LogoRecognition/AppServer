# coding=utf-8
"""Define table and operations for classic goods."""
from sqlalchemy import Column, Integer, VARCHAR, ForeignKey
from . import Base, session, handle_db_exception


class ClassicGoods(Base):
    """Table constructed for classic goods."""
    __tablename__ = 'ClassicGoods'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(VARCHAR(128), nullable=False)
    brand_name = Column(VARCHAR(128), ForeignKey('Brands.name'))
    image = Column(VARCHAR(256), nullable=False)
