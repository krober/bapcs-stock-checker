import datetime

from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.orm import validates

from database.sql_base import Base


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    reddit_id = Column(String(6))
    mpn = Column(String(30))
    price = Column(Integer)
    date = Column(Date)
    site = Column(String(50))

    def __init__(self,
                 reddit_id: str,
                 mpn: str,
                 price: int,
                 date: datetime.date,
                 site: str):
        self.reddit_id = reddit_id
        self.mpn = mpn
        self.price = price
        self.date = date
        self.site = site

    @validates('mpn', 'site')
    def validate_lengths(self, key, value):
        # TODO: add logging of values that violate max_len, likely a parsing error
        """
        For attributes in decorator, check against max value len, and truncate if needed
        :param key: str, passed in from decorator
        :param value: str, passed in by sqlalchemy
        :return: str, the shorter of value and value[:30], further handled by sqlalchemy
        """
        max_len = getattr(self.__class__, key).prop.columns[0].type.length
        if value and len(value) > max_len:
            return value[:max_len]
        return value

    def __repr__(self):
        return f'Post ({self.date} - {self.reddit_id}, {self.mpn})'


