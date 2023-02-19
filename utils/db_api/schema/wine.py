from sqlalchemy import Column, BigInteger, Float, String, Integer, LargeBinary, sql, ForeignKey
from utils.db_api.db_gino import TimedBaseModelCreatedAt


class Wine(TimedBaseModelCreatedAt):

    __tablename__ = 'wine'

    id = Column(BigInteger, primary_key = True, autoincrement=True)
    created_by = Column(BigInteger, ForeignKey('users.id'))
    image = Column(String)
    wine = Column(String)
    score = Column(Float)
    grape = Column(String(30))
    sugar = Column(Integer)
    color = Column(Integer)
    country = Column(String(30))
    producer = Column(String(40))
    year = Column(Integer)
    location = Column(String(120))
    price = Column(Float)
    comment = Column(String(100))

    query: sql.Select