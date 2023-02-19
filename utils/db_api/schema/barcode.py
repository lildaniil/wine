from sqlalchemy import Column, BigInteger, Float, String, Integer, LargeBinary, sql, ForeignKey
from utils.db_api.db_gino import TimedBaseModelCreatedAt


class Barcode(TimedBaseModelCreatedAt):

    __tablename__ = 'barcode'

    id = Column(BigInteger, primary_key = True, autoincrement=True)
    created_by = Column(BigInteger, ForeignKey('users.id'))
    bc_image = Column(String)
    bc_number = Column(String(20))
    type = Column(String(10))
    wine_image = Column(String)