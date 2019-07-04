import logging
import socket
import os

class CrawlerSettings(object):


    # logger
    LOGGER_ID = 'WeiboCrawling'
    LOG_LEVEL = logging.DEBUG
    LOGFILE_BASEPATH = '/Users/caoda1/Documents/news_robot/weibo/logs'
    # LOG_FORMAT = '%(asctime)s - %(name)s (p:%(process)d, %(processName)s) - %(levelname)s - %(message)s'

    LOG_FORMAT = '%(name)s (p:%(process)d, %(processName)s) - %(levelname)s - %(message)s'
    # LOG_FORMAT = '(p:%(processName)s) - %(levelname)s - %(message)s'


    # LOG_FORMAT = '%(asctime)s - [{host} %(name)s (p:%(process)d, %(processName)s) - %(levelname)s - %(message)s]'.format(
    #     host=socket.gethostname()
    # )


    # Paths
    DAEMON_PIDFILE_BASEPATH = '/tmp/'

    MAX_NUM_STATUS_TO_CRAWL = 1000
    MAX_DEGREE_OF_RELATIONS = 3

    NUM_CRAWLER_WORKERS = 4


