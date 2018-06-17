import datetime

from sqlalchemy import Column, Date, Integer, String

from src.sql_base import Base


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    reddit_id = Column(String(6))
    mpn = Column(String(63))
    price = Column(Integer)
    date = Column(Date)
    site = Column(String(63))

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

    def __repr__(self):
        return f'Post ({self.date} - {self.reddit_id}, {self.mpn})'


