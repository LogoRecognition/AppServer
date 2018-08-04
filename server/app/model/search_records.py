# coding=utf-8
"""Define table and operations for search records."""
import datetime
import calendar
from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, DATE, func, desc
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


def get_records_between_dates(brand_name, d1, d2):
    """Get a list of tuple of (year, month, brand name, search counts of that month)."""
    brand_name = brand_name if brand_name else ''
    records = session.query(
        func.year(SearchRecords.date), func.month(SearchRecords.date),
        SearchRecords.brand_name, func.count(SearchRecords.brand_name)) \
        .filter(SearchRecords.brand_name.ilike('%'+brand_name+'%'))\
        .filter(SearchRecords.date.between(d1, d2))\
        .group_by(func.year(SearchRecords.date), func.month(SearchRecords.date), SearchRecords.brand_name)\
        .all()
    print(*records, sep='\n')
    return records


def get_recent_search_champions(brand_name, month_start, month_end):
    try:
        date_end = datetime.datetime.strptime(month_end, "%Y-%m").date() if month_end else datetime.datetime.now()
        date_start = datetime.datetime.strptime(month_start, "%Y-%m").date() if month_start\
            else date_end.replace(year=date_end.year-1)
        # set `date_end` to the end of that month
        date_end = date_end.replace(day=calendar.monthrange(date_end.year, date_end.month)[1])
        records = get_records_between_dates(brand_name, date_start, date_end)
        result = {}
        for record in records:
            temp_date = '%4d-%02d' % (record[0], record[1])
            if result.get(temp_date) is None or result.get(temp_date)['searching_counts'] < record[3]:
                result[temp_date] = {
                    'name': record[2],
                    'searching_counts': record[3]
                }
        session.commit()
        return result
    except Exception as err:
        handle_db_exception(err)
