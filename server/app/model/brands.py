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
