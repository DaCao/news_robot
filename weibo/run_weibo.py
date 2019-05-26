import os
import logging
import signal
from weibo.processors import Processor
from weibo.settings import CrawlerSettings
from daemonize import Daemonize
from psutil import Process
import sys


def start_daemon(processor, logger, file_descriptors):

    daemon = Daemonize(
        app=processor.SYSLOG_NAME,
        pid=processor.pid_path,
        action=processor.start,
        keep_fds=file_descriptors,
        logger=logger,
        foreground=True
    )
    daemon.start()

def stop_daemon(processor, logger):
    try:
        with open(processor.pid_path, 'r') as lockfile:
            running_pid = int(lockfile.read())

    except:
        pass

    logger.warn('Attempting to kill PID: {}'.format(running_pid))
    os.kill(running_pid, signal.SIGTERM)



def main():

    logger = logging.getLogger('WeiboCrawling')
    logger.setLevel(logging.DEBUG)
    log_formatter = logging.Formatter(CrawlerSettings.LOG_FORMAT)

    p = Processor(logger=logger, settings=CrawlerSettings)

    log_handler = logging.StreamHandler(sys.stdout)
    log_handler.setFormatter(log_formatter)
    logger.addHandler(log_handler)

    keep_fds = [log_handler.stream.fileno()]


    proc = Process() # todo: check it out

    start_daemon(p, logger, file_descriptors=keep_fds)



if __name__ == '__main__':
    main()
