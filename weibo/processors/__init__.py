import collections
import json
import multiprocessing
import os
import time
import traceback
import queue
from weibo.settings import CrawlerSettings
from weibo.workers.CrawlerWorker import CrawlerWorker
from weibo.DB.Models.SessionManager import CrawlerSessionManager
import weibo.DB as DB
from weibo.DB.Models.WeiboStatus import MostRecentWeibo, WeiboStatusItem
from sqlalchemy.dialects.mysql import insert
from sqlalchemy import exists


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

        # self.followees = \
        #     [('1895964183', '一起神回复'), ('2134671703', '哈囉李敖'), ('5187664653', '邓超'), ('5501429448', '视觉机器人'),
        #      ('1721030997', '网易云音乐'), ('6049590367', '局座召忠'), ('1182391231', '潘石屹'), ('1192515960', '李冰冰'),
        #      ('1887896087', '广州小资族'), ('1483820045', '尼格买提'), ('3173341643', 'IT数码收录'), ('3952070245', '范冰冰'),
        #      ('1237869662', '南派三叔'), ('1345566427', '佟丽娅'), ('1768305123', '贾静雯'), ('2827050962', '段子坊'),
        #      ('2095230872', '柯泯哲'), ('1743519310', '刘语熙rachel'), ('1198392970', '易中天'), ('1496852380', '崔永元')]

        # self.followees = self.load_users_and_most_recent_weibo()

        self.num_users_left = len(self.followees)

        for i in range(CrawlerSettings.NUM_CRAWLER_WORKERS):
            self.logger.debug('Starting Crawler Worker #{}...'.format(i))
            w = CrawlerWorker(
                jobs_queue = self.jobs_queue,
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
                self.get_idle_worker_and_dispatch_jobs()
            except Exception as e:
                self.logger.debug('get_and_dispatch_work() failed')
                self.logger.debug(e)

            try:
                self.get_and_update_completed_work()
            except Exception as e:
                self.logger.debug('get_and_update_completed_work() failed')
                self.logger.debug(e)

            if self.num_users_left != len(self.followees):
                self.logger.info('self.followees has {} users left.'.format(len(self.followees)))
                self.num_users_left = len(self.followees)

            if len(self.followees) == 0:
                self.logger.info('self.followees has 0 user.')
                return


    def get_idle_worker_and_dispatch_jobs(self):
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
                self.logger.debug('Processor got completed work with {} weibo posts'.format(len(completed_rows)))
            except queue.Empty:
                break


            # write to DB
            try:
                most_recent_row = completed_rows[0]
                self.write_most_recent_weibo(most_recent_row)
            except Exception as e:
                self.logger.debug('processor cannot write most recent weibo to DB')
                print(e)

            try:
                self.write_weibo_status_to_db(completed_rows)
            except Exception as e:
                self.logger.debug('processor cannot write weibo to DB')
                print(e)



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
    def write_weibo_status_to_db(cls, completed_rows):
        sm = CrawlerSessionManager.get_instance()

        with sm.get_session() as session:

            for row in completed_rows:
                session.add(row)

            session.commit()

        return


    @classmethod
    def write_most_recent_weibo(cls, most_recent_row):

        sm = CrawlerSessionManager.get_instance()
        with sm.get_session() as session:

            user_exists = session.query(exists().where(MostRecentWeibo.user_id == most_recent_row.user_id)).scalar()

            if user_exists:
                session.query(MostRecentWeibo).filter_by(user_id = most_recent_row.user_id).\
                    update({'user_name': most_recent_row.user_name,
                            'status_id': most_recent_row.status_id,
                            'creation_time': most_recent_row.creation_time,
                            'text': most_recent_row.text})
            else:
                row = MostRecentWeibo(user_id = most_recent_row.user_id,
                                        user_name = most_recent_row.user_name,
                                        status_id = most_recent_row.status_id,
                                        creation_time = most_recent_row.creation_time,
                                        text = most_recent_row.text
                                )
                session.add(row)

            session.commit()

        return



    def load_users_and_most_recent_weibo(self):

        sm = CrawlerSessionManager.get_instance()

        with sm.get_session() as session:
            items = session.query(MostRecentWeibo.user_id, MostRecentWeibo.user_name, MostRecentWeibo.status_id)

        print(type(items))
        return items