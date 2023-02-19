from sqlalchemy import Integer, Column, BigInteger, String, BOOLEAN, sql
from utils.db_api.db_gino import TimedBaseModel, BaseModel


class User(TimedBaseModel):

    __tablename__ = 'users'

    id = Column(BigInteger, primary_key = True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    username = Column(String(100))
    language_code = Column(String(10))
    is_bot = Column(BOOLEAN)
    is_premium = Column(BOOLEAN)
    added_to_attachment_menu = Column(BOOLEAN)
    can_join_groups = Column(BOOLEAN)
    can_read_all_group_messages = Column(BOOLEAN)
    supports_inline_queries = Column(BOOLEAN)

    refferal = Column(BigInteger)

    query: sql.Select