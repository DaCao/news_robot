import collections
import json
import multiprocessing
import os
import queue
import time
import traceback
from weibo.settings import CrawlerSettings
from weibo.workers.CrawlerWorker import CrawlerWorker
from weibo.DB.Models.SessionManager import CrawlerSessionManager
import weibo.DB as DB


class WeiboCrawlProcessor(object):

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

        # initialize DB
        DB.initialize()

        self.logger.info("Starting {} processor...".format(self.SYSLOG_NAME))
        self.jobs_queue = multiprocessing.Queue()
        self.result_queue = multiprocessing.Queue()

        with open('/Users/caoda1/Documents/news_robot/weibo/followees.json', 'r') as f:
            followees_dict = json.load(f)

        self.followees = list(followees_dict.items())
        self.users_left = len(self.followees)
        # self.followees = self.followees[:10] # todo: delete

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

            # self.get_and_update_completed_work()

            try:
                self.get_and_update_completed_work()
            except Exception as e:
                self.logger.debug('get_and_update_completed_work() failed')
                self.logger.debug(e)

            if self.users_left != len(self.followees):
                print('fuck  ', len(self.followees))
                self.users_left = len(self.followees)


            if len(self.followees) == 0:
                self.logger.info('self.followees has 0 user.')
                return


    def get_and_dispatch_work(self):
        # get number of idle workers
        idle_workers = self._get_idle_workers()
        # dispatch jobs to idle workers
        if len(idle_workers) > 0:
            for i in range(len(idle_workers)):
                item = self.followees.pop()
                self.logger.debug('putting {} into processor jobs_queue...'.format(item))
                self.jobs_queue.put(item)


    def get_and_update_completed_work(self):

        while True:
            try:
                completed_rows = self.result_queue.get(block=False) # todo:  setting block=False is so fucking important
            # except Exception as e:
            except queue.Empty:
                # self.logger.debug('result_queue is empty!   ')
                break


            self.logger.debug('Processor got completed work {} '.format(completed_rows))
            # if row object generation was successful, attempt to write rows within a transaction

            self.write_course_records(completed_rows)

            # write to DB
            # try:
            #     self.write_course_records(completed_rows)
            # except Exception as e:
            #     print(e)
            #     break



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



    @classmethod
    def write_course_records(cls, completed_rows):
        sm = CrawlerSessionManager.get_instance()

        with sm.get_session() as session:

            for row in completed_rows:
                session.add(row)

            session.commit()



        return



