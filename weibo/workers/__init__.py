import ctypes
import multiprocessing
import traceback
from weibo_api.client import WeiboClient

class Worker(multiprocessing.Process):

    SYSLOG_NAME = 'WeiboWorker'

    def __init__(self, work_queue, output_queue, logger, settings, worker_number):
        self.name = '{}_{}'.format(self.SYSLOG_NAME, worker_number)
        self.queue = work_queue
        self.output_queue = output_queue
        self.logger = logger
        self.settings = settings
        self.current_item = None

        # worker states
        self.idle = multiprocessing.Value(ctypes.c_bool, True)

        super().__init__()

    def run(self):

        while True:

            try:
                self.worker_loop()
            except Exception as e:
                self.logger.error('Exception encountered while processing {}. Error: {}'.format(
                    self.current_item, str(e)
                ))

                self.logger.error(traceback.format_exc())

                self.logger.info('Setting worker state to idle after unhandled exception...')
                self._set_idle()



    def worker_loop(self):
        raise NotImplementedError()

    def perform_work(self):
        raise  NotImplementedError()

    def _set_idle(self):
        with self.idle.get_lock():
            self.idle.value = True

    def _set_busy(self):
        with self.idle.get_lock():
            self.idle.value = False