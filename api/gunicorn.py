"""Configuration file for gunicorn, As we are using init hooks,
we need to keep this file in python (see
https://github.com/benoitc/gunicorn/blob/master/examples/example_config.py)
for an example.
"""
import datetime
import logging
import multiprocessing
import sys

from app import create_app

workers = multiprocessing.cpu_count() + 1
timeout = 2000


def on_starting(_):
    """This is a gunicorn hook that is run once upon starting the server.
    We use this hook to setup the initial data creation, right now those are
    run upon app creation, so we just create a dummy application to trigger
    those hooks
    """

    # the logging system will be confirgured at app creation,
    # so, don't use it before
    print(f"{datetime.datetime.now()}: Running the startup hook ", flush=True)

    # initialize the local cache of the datasets
    create_app(on_startup=True)

    logging.info("startup hook finished")
    #  Explicitely flush so that we have the init logs
    sys.stdout.flush()
