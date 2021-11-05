import logging
import time
from subprocess import run

import schedule


def module_logger(mod_name: str):
    logger = logging.getLogger(mod_name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s [%(name)-12s] %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger


log = module_logger(__name__)


def fetch_pull_job():
    """Job to be scheduled to handle fetching and pulling from the remote"""
    log.info('Executing /root/scripts/fetch-pull')
    run(['sh', '/root/scripts/fetch-pull'])


def push_job():
    """Job to be scheduled to handle pushing to the remote"""
    log.info('Executing /root/scripts/push')
    run(['sh', '/root/scripts/push'])


if __name__ == '__main__':
    schedule.every().hour.at(':00').do(fetch_pull_job)
    schedule.every().hour.at(':05').do(push_job)

    while True:
        schedule.run_pending()
        time.sleep(30)
