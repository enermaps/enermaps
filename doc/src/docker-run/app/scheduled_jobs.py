import time
from os import environ as env
from subprocess import run

import schedule

from . import module_logger
from .editor_auth_handler import get_authenticated_user_string

log = module_logger(__name__)


def fetch_pull_job():
    """Job to be scheduled to handle fetching and pulling from the remote"""
    log.info('Executing /root/scripts/fetch-pull')
    run(['sh', '/root/scripts/fetch-pull'])


def push_job():
    """Job to be scheduled to handle pushing to the remote"""
    log.info('Executing /root/scripts/push')
    run(['sh', '/root/scripts/push'])


def refresh_auth_users():
    """Job to be scheduled to handle syncing the users with edit rights to the wiki"""
    log.info('Refreshing AUTH_USERS')
    auth_users = get_authenticated_user_string()
    log.info(f'AUTH_USERS={auth_users}')
    env['AUTH_USERS'] = auth_users


if __name__ == '__main__':
    schedule.every().hour.at(':00').do(fetch_pull_job)
    schedule.every().hour.at(':05').do(push_job)
    schedule.every().hour.at(':10').do(refresh_auth_users)

    while True:
        schedule.run_pending()
        time.sleep(30)
