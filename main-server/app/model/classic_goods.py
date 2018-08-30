# coding=utf-8
"""Define table and operations for classic goods."""
from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, UniqueConstraint, and_
from . import Base, session, handle_db_exception


class ClassicGoods(Base):
    """Table constructed for classic goods."""
    __tablename__ = 'ClassicGoods'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(VARCHAR(128), nullable=False)
    brand_name = Column(VARCHAR(128), ForeignKey('Brands.name'))
    image = Column(VARCHAR(256), nullable=False)

    UniqueConstraint(brand_name, name)


def add_classic_goods(name, brand_name, image):
    try:
        goods = ClassicGoods()
        goods.name = name
        goods.brand_name = brand_name
        goods.image = image
        session.add(goods)
        session.commit()
    except Exception as err:
        handle_db_exception(err)


def find_single_classic_goods(name, brand_name):
    try:
        the_goods = session.query(ClassicGoods).filter(
            and_(ClassicGoods.name.ilike('%'+name+'%'), ClassicGoods.brand_name.ilike('%'+brand_name+'%')))\
            .first()
        session.commit()
        return the_goods
    except Exception as err:
        handle_db_exception(err)


def find_list_of_classic_goods_by_brand_name(brand_name):
    try:
        list_of_goods = session.query(ClassicGoods).filter(ClassicGoods.brand_name.ilike('%'+brand_name+'%')).all()
        session.commit()
        return list_of_goods
    except Exception as err:
        handle_db_exception(err)
