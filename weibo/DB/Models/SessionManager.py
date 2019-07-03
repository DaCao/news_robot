from functools import partial
from collections import defaultdict
from contextlib import contextmanager
from threading import Thread, Lock, Event
import traceback

from sqlalchemy import create_engine, MetaData
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import sessionmaker, scoped_session


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

    def get_instance(cls):
        return cls._instances[cls]


class CrawlerSessionManager(object, metaclass=Singleton):

    def __init__(self, db_config):
        """

        :param db_config: Database config, consisting of known SQLAlchemy config key/values
        :param pool_args:
        :param kwargs:
        """
        self._db_config = db_config

        self._engine = None
        self._engine_string = None


    def build_db_engine_string(self, user, password, host, port=3306, engine='mysql', db=None, charset='utf8mb4'):
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


        if db is None:
            # empty db name, parameters cannot directly follow port
            conn_string += '/'
        else:
            conn_string += '/{db}'.format(db=db)

        # append charset param
        conn_string += '?charset={}'.format(charset)

        return conn_string

    @contextmanager
    def get_session(self, autoflush=True, autocommit=False):
        """
        :param company_id:
        :param db_type:
        :param autoflush:
        :param autocommit:
        :return:
        """

        session = scoped_session(sessionmaker(autoflush=autoflush, autocommit=autocommit, bind=self._engine))

        try:
            yield session
        finally:
            session.remove()



    def populate_engines(self):
        """
        Populate the session manager's internal engine mapping. The CrawlerSessionManager

        :return:
        """

        self._engine_string = self.build_db_engine_string(
            user=self._db_config['user'],
            password=self._db_config['password'],
            host=self._db_config['host'],
            port=self._db_config['port'],
            db=self._db_config['db'],
            charset='utf8mb4'
        )

        self._engine = create_engine(self._engine_string)





