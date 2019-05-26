import collections
import json
import multiprocessing
import os
import queue
import time
import traceback
from weibo.settings import CrawlerSettings
from weibo.workers.CrawlerWorker import CrawlerWorker


class Processor(object):

    SYSLOG_NAME = 'WeiboProcessor'

    def __init__(self, logger, settings):
        self.logger = logger
        self.settings = settings

        self.workers = []
        self.jobs_queue = []
        self.result_queue = []

    def start(self):
        """

        :return:
        """

        self.logger.info("Starting {} processor...".format(self.SYSLOG_NAME))
        self.jobs_queue = multiprocessing.Queue()
        self.result_queue = multiprocessing.Queue()

        with open('/Users/caoda1/Documents/news_robot/weibo/followees.json', 'r') as f:
            followees_dict = json.load(f)

        self.followees = list(followees_dict.items())

        for i in range(CrawlerSettings.NUM_CRAWLER_WORKERS):
            self.logger.debug('Starting Crawler Worker #{}...'.format(i))
            w = CrawlerWorker(
                work_queue = self.jobs_queue,
                output_queue = self.result_queue,
                logger = self.logger,
                settings = self.settings,
                worker_number = i)

            w.daemon = True
            w.start()
            self.workers.append(w)

        self.run()


    def run(self):
        """

        :return:
        """
        self.logger.debug('{} running'.format(type(self).__name__))

        while True:

            try:
                self.get_and_dispatch_work()
            except Exception as e:
                self.logger.debug('get_and_dispatch_work() failed')
                self.logger.debug(e)

            try:
                self.get_and_update_completed_work()
            except Exception as e:
                self.logger.debug('get_and_update_completed_work() failed')
                self.logger.debug(e)


    def get_and_dispatch_work(self):
        # get number of idle workers
        idle_workers = self._get_idle_workers()

        # dispatch jobs to idle workers
        if len(idle_workers) > 0:
            for i in range(len(idle_workers)):
                self.jobs_queue.put(self.followees.pop())



    def get_and_update_completed_work(self):
        while True:
            try:
                completed_item = self.result_queue.get()
            except Exception as e:
                break
                # self.logger.debug('Failing to get result...')
                # self.logger.debug(e)


    def _get_idle_workers(self):
        """
        :return:
        """
        idle = []
        for w in self.workers:
            with w.idle.get_lock():
                if w.idle.value:
                    idle.append(w)
        return idle

    @property
    def pid_path(self):
        return os.path.join(self.settings.DAEMON_PIDFILE_BASEPATH, '{}.pid'.format(self.SYSLOG_NAME))





