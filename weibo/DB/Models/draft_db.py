from functools import partial
from collections import defaultdict
from contextlib import contextmanager
from threading import Thread, Lock, Event
import traceback

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import sessionmaker, scoped_session



def build_db_engine_string(user, password, host, port=3306, engine='mysql', db=None, charset=None):
    """

    :param user:
    :param password:
    :param host:
    :param port:
    :param engine:
    :param db:
    :param charset:
    :return:
    """

    conn_string = '{engine}://{user}:{password}@{host}:{port}'.format(
        engine=engine,
        user=user,
        password=password,
        host=host,
        port=port
    )

    if db is not None:
        conn_string += '/{db}'.format(db=db)

    if charset is not None:
        if db is None:
            # empty db name, parameters cannot directly follow port
            conn_string += '/'
        # append charset param
        conn_string += '?charset={}'.format(charset)

    return conn_string


def make_them(metadata):

    user_table = Table('user', metadata,
                       Column('id', Integer, primary_key=True),
                       Column('name', String(50)),
                       Column('fullname', String(100))
                       )

    address_table = Table('address', metadata,
                          Column('id', Integer, primary_key=True),
                          Column('user_id', None, ForeignKey('user.id')),
                          Column('email', String(128), nullable=False)
                          )

    metadata.create_all()

    return


if __name__ == '__main__':
    conn_string = build_db_engine_string(user='root',
                                         password='',
                                         host='127.0.0.1',
                                         db='test')

    print(type(conn_string), conn_string)

    engine = create_engine(conn_string)
    metadata = MetaData(engine)

    #make_them(metadata)

    conn = engine.connect()


    user_table = Table('user', metadata, autoload=True)
    ins = user_table.insert()
    print(type(ins), ins)

    for i in range(10):

        ins = ins.values(name='adam', fullname='Adam Gu')
        print(ins)

        conn.execute(ins)
