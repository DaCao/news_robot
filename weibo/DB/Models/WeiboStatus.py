import datetime
from sqlalchemy import Column, ForeignKey, text
from sqlalchemy.dialects.mysql import BIGINT, VARCHAR, DATETIME, INTEGER, LONGTEXT, TEXT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from weibo.DB.Models.Followee import Followees

BASE = declarative_base()

class WeiboStatusItem(BASE):
    __tablename__ = 'user_weibo_status'

    status_id = Column('status_id', VARCHAR(60), primary_key=True)
    # user_id = Column('user_id', VARCHAR(60), ForeignKey('followees.uid'))
    # user_name = Column('user_name', VARCHAR(60), ForeignKey('followees.name'))

    user_id = Column('user_id', VARCHAR(60))
    user_name = Column('user_name', VARCHAR(60))

    creation_time = Column('creation_time', VARCHAR(60), nullable=False, default='')
    # text = Column('text', LONGTEXT(collation='utf8'), nullable=True, default=None)
    text = Column('text', TEXT, nullable=True, default=None)
    reposts_count = Column('reposts_count', TEXT)
    attitudes_count = Column('attitudes_count', INTEGER)
    comments_count = Column('comments_count', INTEGER)
    source = Column('source', TEXT) # todo: maybe other text type...

    # units = relationship('followee')




