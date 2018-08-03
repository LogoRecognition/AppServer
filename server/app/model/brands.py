# coding=utf-8
"""Define table and operations for brands."""
from sqlalchemy import Column, Integer, VARCHAR, TEXT
from . import Base, session, handle_db_exception


class Brands(Base):
    """Table constructed for brands."""
    __tablename__ = 'Brands'

    name = Column(VARCHAR(128), primary_key=True, nullable=False, unique=True)
    intro = Column(TEXT, nullable=False)
    category = Column(VARCHAR(128), nullable=False)
    logo = Column(VARCHAR(256), nullable=False)


def add_brand(_name, _category, _logo, _intro):
    """Add a brand to database."""
    brand = Brands()
    brand.name = _name
    brand.intro = _intro
    brand.category = _category
    brand.logo = _logo
    try:
        session.add(brand)
        session.commit()
    except Exception as err:
        handle_db_exception(err)
