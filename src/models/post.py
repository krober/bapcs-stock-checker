import datetime

from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.orm import validates

from logger import logger
from database.sql_base import Base


class Post(Base):
    """
    Represents a reddit post with additional data
    :attr id: Integer, generated sql pk
    :attr reddit_fullname: str, reddit type identifier 't3_' + submission id ex. 'a4hafgh'
    :attr mpn: str, manufacturer part number for linked product
    :attr price: int, rounded price of product at date of instantiation
    :attr date: Date, date of instantiation
    :attr site: str, domain of linked product ex 'microcenter.com'
    """
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    reddit_fullname = Column(String(15), nullable=False, unique=True)
    mpn = Column(String(30))
    price = Column(Integer)
    date = Column(Date)
    site = Column(String(50))

    post_logger = logger.get_logger('Post', './logfile.log')

    def __init__(self,
                 reddit_fullname: str,
                 mpn: str,
                 price: int,
                 date: datetime.date,
                 site: str,
                 ):
        self.reddit_fullname = reddit_fullname
        self.mpn = mpn
        self.price = price
        self.date = date
        self.site = site

    @validates('mpn', 'site')
    def validate_lengths(self, key, value):
        """
        For attributes in decorator, check against max value len, and truncate if needed
        :param key: str, each str passed in from decorator
        :param value: str, passed in by sqlalchemy
        :return: str, the shorter of value and value[:30], further handled by sqlalchemy
        """
        max_len = getattr(self.__class__, key).prop.columns[0].type.length
        if value and len(value) > max_len:
            self.post_logger.info(f'{key}: {value} - violated max length and was truncated')
            return value[:max_len]
        return value

    def __repr__(self):
        return f'Post ({self.date} - {self.reddit_fullname}, {self.mpn})'


if __name__ == '__main__':
    pass


