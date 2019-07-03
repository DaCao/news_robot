import datetime
from sqlalchemy import Column, ForeignKey, text
from sqlalchemy.dialects.mysql import BIGINT, VARCHAR, DATETIME, INTEGER, LONGTEXT, TEXT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

BASE = declarative_base()

class Followees(BASE):

    __tablename__ = 'followees'

    uid = Column('uid', VARCHAR(60), primary_key=True)
    name = Column('status_id', VARCHAR(60), primary_key=True)
    creation_time = Column('creation_time', DATETIME, nullable=False, default=datetime.datetime.utcnow)
    last_update_time = Column('last_update_time', DATETIME, nullable=False, default=datetime.datetime.utcnow)
    last_update_status = Column('last_update_status', LONGTEXT(collation='utf8_bin'), nullable=True, default=None)

    followers_count = Column('followers_count', INTEGER)
    followees_count = Column('followees_count', INTEGER)
    status_count = Column('status_count', INTEGER)

