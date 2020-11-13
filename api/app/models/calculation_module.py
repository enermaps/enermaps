import re
import json
from celery import Celery, result
import logging
import redis
import json

import kombu
from celery import Celery
import celery


# TODO; migrate this to pyparsing maybe ?
INFO_STRING = re.compile("^(?P<task_id>[a-zA-Z._]+) \\[cm_info=(?P<task_info>.+)\\]$")


def get_celery_app():
    app = Celery(broker="redis://guest@redis//", backend="redis://redis")
    app.conf.update(
        task_serializer="json",
        accept_content=["json"],  # Ignore other content
        result_serializer="json",
        timezone="Europe/Zurich",
        enable_utc=True,
    )
    transport_options = {}
    transport_options['max_retries'] = 3
    transport_options['interval_start'] = 0.5
    transport_options['interval_step'] = 1
    transport_options['interval_max'] = 2
    app.conf.update(broker_transport_options=transport_options)
    return app


def task_by_id(task_id, cm_name):
    app = get_celery_app()
    res = app.AsyncResult(task_id, task_name=cm_name)
    return res


def list_cms():
    app = get_celery_app()
    try:
        app_inspector = app.control.inspect()
        nodes = app_inspector.registered("cm_info")
    except (redis.exceptions.ConnectionError, kombu.exceptions.OperationalError) as err:
        # If redis is down, we just don't expose any calculation module
        logging.error("Connection to celery broken resulted in an error: ", err)
        return {}
    if not nodes:
        nodes = {}
    cms = {}
    for node in nodes.values():
        for entry in node:
            task = from_registration_string(entry)
            cms[task.task_id] = task
    return cms


def cm_by_name(cm_name):
    cms = list_cms()
    try:
        cm = cms[cm_name]
    except KeyError:
        raise Exception("Cannot find calculation module {}".format(cm_name))
    return cm


def from_registration_string(registration_string):
    r = INFO_STRING.match(registration_string)
    if not r:
        raise Exception(
            "invalid parameters used for creating a CM:" + registration_string
        )

    task_id = r.group("task_id")
    raw_task_info = r.group("task_info")
    try:
        task_info = json.loads(raw_task_info)
    except json.JSONDecodeError:
        raise Exception(
            "invalid task_info property when creating a CM:"
            + raw_task_info
            + " for cm "
            + task_id
        )
    return CalculationModule(task_id, **task_info)


class CalculationModule:
    def __init__(self, task_id, **kwargs):
        self.app = get_celery_app()
        self.task_id = task_id
        self.params = kwargs
        self.__doc__ = kwargs.get(
            "doc", "no documentation available for this calculation module"
        )

    def call(self, *args, **kwargs):
        return self.app.send_task(self.task_id, args, kwargs)

    def get_task(self, task_id):
        pass

    def __dict__(self):
        {"name": self.task_id}
