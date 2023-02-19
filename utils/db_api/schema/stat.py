from sqlalchemy import Column, BigInteger, String, sql, ForeignKey
from utils.db_api.db_gino import TimedBaseModelCreatedAt


class Statistic(TimedBaseModelCreatedAt):

    __tablename__ = 'statistics'

    id = Column(BigInteger, primary_key = True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id'))
    action = Column(String(20))
    action_data = Column(String(100))

    query: sql.Select