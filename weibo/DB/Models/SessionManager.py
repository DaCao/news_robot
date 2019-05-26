
from collections import defaultdict
from contextlib import contextmanager
from threading import Thread, Lock, Event
import traceback

from sqlalchemy import create_engine
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import sessionmaker, scoped_session



class SessionManager(object):

    _engines = {}
    _db_config = None
    _pool_args = None

    def __init__(self, db_config: dict, pool_args: dict=None, **kwargs):
        """

        :param db_config: Database config, consisting of known SQLAlchemy config key/values
        :param pool_args:
        :param kwargs:
        """

        self._engines = None
        self._db_config = db_config
        self._pool_args = pool_args


    def build_db_engine_string(self, user, password, host, port=3306, engine='mysql', db=None, charset=None):
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

    def get_session(self, company_id, db_type, autoflush=True, autocommit=False):
        raise NotImplementedError

    def populate_engines(self):
        raise NotImplementedError







