import datetime
from sqlalchemy import Column, ForeignKey, text
from sqlalchemy.dialects.mysql import BIGINT, VARCHAR, DATETIME, INTEGER, LONGTEXT, TEXT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from weibo.DB.Models.Followee import Followees

BASE = declarative_base()

class WeiboStatus(BASE):

    __tablename__ = 'user_weibo_status'

    status_id = Column('status_id', VARCHAR(60), primary_key=True)

    user_id = Column('user_id', VARCHAR(60), ForeignKey('followees.uid'))
    user_name = Column('user_name', VARCHAR(60), ForeignKey('followees.name'))
    creation_time = Column('creation_time', DATETIME, nullable=False, default=datetime.datetime.utcnow)
    text = Column('text', LONGTEXT(collation='utf8_bin'), nullable=True, default=None)
    reposts_count = Column('reposts_count', INTEGER)
    attitudes_count = Column('attitudes_count', INTEGER)
    comments_count = Column('comments_count', INTEGER)
    source = Column('source', TEXT) # todo: maybe other text type...

    units = relationship('followee')

