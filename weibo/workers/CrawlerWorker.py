import ctypes
import multiprocessing
from weibo_api.client import WeiboClient
from weibo.DB.Models.WeiboStatus import WeiboStatusItem


class CrawlerWorker(multiprocessing.Process):

    SYSLOG_NAME = 'CrawlerWorker'

    def __init__(self, jobs_queue, output_queue, logger, settings, worker_number):

        # get weibo api connection
        self.client = WeiboClient()

        self.name = '{}_{}'.format(self.SYSLOG_NAME, worker_number)
        self.jobs_queue = jobs_queue
        self.output_queue = output_queue
        self.logger = logger
        self.settings = settings
        self.current_item = None

        # worker states
        self.idle = multiprocessing.Value(ctypes.c_bool, True)

        super().__init__()


    def run(self):
        while True:
            self.worker_loop()


    def worker_loop(self):

        try:

            if self.jobs_queue.empty():
                self._set_idle()
                self.logger.info('{} has empty jobs_queue, and is set to idle! '.format(self.name))
                return

            self.current_item = self.jobs_queue.get()
            self._set_busy()
            self.logger.info('{} got user {}, and set to busy.'.format(self.name, self.current_item))
            name, rows = self.perform_work()
            self.output_queue.put(rows)
            self.logger.info('{} finished working on {}'.format(self.name, name))

        except Exception as e:
            self.logger.error('{} has worker_loop error:'.format(self.name))
            print(e)
            self._set_idle()
            self.logger.info('{} is set to idle! '.format(self.name))


    def perform_work(self):
        id, name = self.current_item
        p = self.client.people(uid=id)

        rows = []

        # for status in p.statuses.all():
        # for status in p.statuses.page(1):
        for status in p.statuses.page_from_to(1, 100):

            self.logger.info('{} got {}\'s status on {}, text type is {}'.format(self.name, p.name, status.created_at,
                                                                                 type(status.text)))

            # print(u"微博动态：{}".format(status.id))
            # print(u"发布时间：{}".format(status.created_at))
            # print(u"微博内容概要：{}".format(status.text))
            # print(u"转发数：{}".format(status.reposts_count))
            # print(u"点赞数：{}".format(status.attitudes_count))
            # print(u"评论数：{}".format(status.comments_count))
            # print(u"发布于：{}".format(status.source))
            # print("==================================================")

            rows.append(WeiboStatusItem(
                status_id = status.id,
                user_id = p.name,
                creation_time = status.created_at,
                text = status.text,
                reposts_count = status.reposts_count,
                attitudes_count = status.attitudes_count,
                comments_count = status.comments_count,
                source = status.source
            ))

        return name, rows


    def _set_idle(self):
        with self.idle.get_lock():
            self.idle.value = True

    def _set_busy(self):
        with self.idle.get_lock():
            self.idle.value = False




if __name__ == '__main__':

    print(CrawlerWorker.mro())


