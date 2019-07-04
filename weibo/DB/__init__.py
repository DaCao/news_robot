import datetime
from sqlalchemy import Column, ForeignKey, text
from sqlalchemy.dialects.mysql import BIGINT, VARCHAR, DATETIME, INTEGER, LONGTEXT, TEXT, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import sessionmaker, scoped_session

from weibo.DB.Models.Followee import Followees
from weibo.DB.Models.SessionManager import CrawlerSessionManager
from weibo.DB.Models.WeiboStatus import WeiboStatusItem, MostRecentWeibo



db_config = {
    'user':'root',
    'password':'',
    'host':'127.0.0.1',
    'port': 3306,
    'db': 'weibo'
}


def initialize():

    engine = create_engine('mysql://root@127.0.0.1:3306/weibo')
    metadata = MetaData(engine)

    # nuke
    # metadata.drop_all(bind=engine, tables=[WeiboStatusItem.__table__])
    WeiboStatusItem.__table__.drop(engine)
    MostRecentWeibo.__table__.drop(engine)


    # if not engine.dialect.has_table(engine, 'user'):  # If table don't exist, Create.
    #
    #     Table('user', metadata,
    #           Column('id', Integer, primary_key=True),
    #           Column('name', String(50)),
    #           Column('fullname', String(100))
    #           )

    # if not engine.dialect.has_table(engine, 'followees'):  # If table don't exist, Create.
    #
    #     Table('followees', metadata,
    #         Column('uid', VARCHAR(60), primary_key=True),
    #         Column('status_id', VARCHAR(60), primary_key=True),
    #         Column('creation_time', DATETIME, nullable=False, default=datetime.datetime.utcnow),
    #         Column('last_update_time', DATETIME, nullable=False, default=datetime.datetime.utcnow),
    #         Column('last_update_status', LONGTEXT(collation='utf8_bin'), nullable=True, default=None),
    #
    #         Column('followers_count', INTEGER),
    #         Column('followees_count', INTEGER),
    #         Column('status_count', INTEGER)
    #         )

    if not engine.dialect.has_table(engine, 'user_weibo_status'):  # If table don't exist, Create.

        Table('user_weibo_status', metadata,

            Column('status_id', VARCHAR(60), primary_key=True),

            # Column('user_id', VARCHAR(60), ForeignKey('followees.uid')),
            # Column('user_name', VARCHAR(60), ForeignKey('followees.name')),

            Column('user_id', VARCHAR(60)),
            Column('user_name', VARCHAR(60)),

            Column('user_name', VARCHAR(60)),
            Column('creation_time', VARCHAR(60), nullable=False, default=''),
            Column('text', TEXT, nullable=True, default=None),
            Column('reposts_count', INTEGER),
            Column('attitudes_count', INTEGER),
            Column('comments_count', INTEGER),
            Column('source', TEXT),
        )

    if not engine.dialect.has_table(engine, 'user_most_recent_weibo'):  # If table don't exist, Create.

        Table('user_most_recent_weibo', metadata,
            Column('user_id', VARCHAR(60), primary_key=True),
            Column('user_name', VARCHAR(60)),
            Column('status_id', VARCHAR(60)),
            Column('creation_time', VARCHAR(60), nullable=False, default=''),
            Column('text', TEXT, nullable=True, default=None)
        )


    metadata.create_all()

    mgr = CrawlerSessionManager(db_config)

    mgr.populate_engines()

    return


"""
Could not initialize target column for ForeignKey 'followees.name' on table 'user_weibo_status': table 'followees' has no column named 'name'
"""

