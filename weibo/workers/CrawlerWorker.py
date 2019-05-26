import ctypes
import multiprocessing
import traceback
from weibo_api.client import WeiboClient

from weibo.workers import Worker

class CrawlerWorker(Worker):

    SYSLOG_NAME = 'CrawlerWorker'

    def __init__(self, work_queue, output_queue, logger, settings, worker_number):

        # get weibo api connection
        self.client = WeiboClient()

        super().__init__(work_queue, output_queue, logger, settings, worker_number)


    def run(self):
        super().run()


    def worker_loop(self):

        self.current_item = self.queue.get()
        self._set_busy()
        self.logger.info('{} got user {}'.format(self.name, self.current_item))

        try:
            completed_item = self.perform_work()
            self.output_queue.put(completed_item)
            self.logger.info('{} finished working on {}'.format(self.name, completed_item))
        except:
            pass


    def perform_work(self):
        id, name = self.current_item
        p = self.client.people(uid=id)

        try:
            for status in p.statuses.page(1):
                self.logger.info('{} got {}\'s status on {}'.format(self.name, p.name, status.created_at))
                # print(u"微博动态：{}".format(status.id))
                # print(u"发布时间：{}".format(status.created_at))
                # print(u"微博内容概要：{}".format(status.text))
                # print(u"转发数：{}".format(status.reposts_count))
                # print(u"点赞数：{}".format(status.attitudes_count))
                # print(u"评论数：{}".format(status.comments_count))
                # print(u"发布于：{}".format(status.source))
                # print("==================================================")
                # break

        except:
            pass


        return name

