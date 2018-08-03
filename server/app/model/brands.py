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

    def to_json(self):
        """Return a json for the record."""
        return {
            'name': self.name,
            'intro': self.intro,
            'category': self.category,
            'logo': self.logo
        }


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


def find_brand_by_name(_name):
    try:
        the_brand = session.query(Brands).filter(Brands.name == _name).first()
        session.commit()
        return the_brand
    except Exception as err:
        handle_db_exception(err)


def find_brands_by_name_list(names):
    the_brands = [session.query(Brands).filter(Brands.name == name).first() for name in names]
    return the_brands
