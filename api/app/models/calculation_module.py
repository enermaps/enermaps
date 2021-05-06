"""This module abstract calculation module and task ran on those.
A calculation module is a long ran operation (from minutes of runtime to hours)
That uses one or multiple raster file and a multipolygon that is used as a
selection.
"""
import json
import logging
import os
import re
from typing import Dict, Text

import kombu
import redis
from celery import Celery

TASK_MATCH = "(?P<cm_id>[ a-zA-Z._]+)"
CM_INFO_MATCH = "\\[cm_info=(?P<cm_info>.+)\\]"
INFO_STRING = re.compile("^" + TASK_MATCH + " " + CM_INFO_MATCH + "$")

DEFAULT_BROKER = "redis://localhost"
DEFAULT_BACKEND = "redis://localhost"


def get_celery_app():
    """Return an instance of a celery application using either the
    default settings taken from DEFAULT_* in this module scope or from the
    corresponding environment variables.
    """
    broker = os.environ.get("CELERY_BROKER_URL", DEFAULT_BROKER)
    backend = os.environ.get("CELERY_RESULT_BACKEND", DEFAULT_BACKEND)
    app = Celery(broker=broker, backend=backend)
    app.conf.update(
        task_serializer="json",
        accept_content=["json"],  # Ignore other content
        result_serializer="json",
        timezone="Europe/Zurich",
        enable_utc=True,
    )
    transport_options = {}
    transport_options["max_retries"] = 3
    transport_options["interval_start"] = 0.5
    transport_options["interval_step"] = 1
    transport_options["interval_max"] = 2
    app.conf.update(broker_transport_options=transport_options)
    return app


def task_by_id(task_id, cm_name):
    """Return a task by id and calculation module name"""
    app = get_celery_app()
    res = app.AsyncResult(task_id, task_name=cm_name)
    return res


class CalculationModule:
    """This class describes a remote long running task, also called a
    calculation module.
    """

    def __init__(self, cm_id, **kwargs):
        self.app = get_celery_app()
        self.cm_id = cm_id
        self.name = kwargs.get("name", cm_id)
        self.pretty_name = kwargs.get("pretty_name", self.name)
        self.params = kwargs
        self.schema = kwargs.get("schema", {})
        self.__doc__ = kwargs.get(
            "doc", "no documentation available for this calculation module"
        )

    def call(self, *args, **kwargs):
        """Call the calculation module and return the created task id as a string.
        this task id serves as a reference for getting the status of the task
        (failure, running or done) and its results.
        """
        return self.app.send_task(self.cm_id, args, kwargs)


def list_cms() -> Dict[Text, CalculationModule]:
    """List all cms available on a celery queue."""
    app = get_celery_app()
    try:
        app_inspector = app.control.inspect()
        nodes = app_inspector.registered("cm_info")
    except (redis.exceptions.ConnectionError, kombu.exceptions.OperationalError) as err:
        # If redis is down, we just don't expose any calculation module
        logging.error("Connection to celery broker failed with error: %s", err)
        return {}
    if not nodes:
        return {}
    cms = {}
    for node in nodes.values():
        for entry in node:
            try:
                cm = from_registration_string(entry)
            except InvalidRegistrationString as e:
                # invalid cm was encountered, skip it
                logging.error(e)
                continue
            cms[cm.name] = cm
    return cms


class UnexistantCalculationModule(Exception):
    """Exception thrown for a non-existing calculation module"""

    pass


def cm_by_name(cm_name):
    """Return a single cm by name.

    Raise an UnexistantCalculationModuleException if it cannot be found.
    """
    cms = list_cms()
    try:
        calculation_module = cms[cm_name]
    except KeyError:
        raise UnexistantCalculationModule(
            "Cannot find calculation module {}".format(cm_name)
        )
    return calculation_module


class InvalidRegistrationString(Exception):
    """Exception raised by from_registration_string upon encountering
    an invalid registration string"""

    pass


def from_registration_string(registration_string):
    """Create an instance of a calculation module based upon
    a registration string.
    This string is passed from the task to the broker and must be
    matched by the INFO_STRING regexp.

    raises an exception if the calculation module string cannot be parsed.
    """
    registration_string_match = INFO_STRING.match(registration_string)
    if not registration_string_match:
        raise InvalidRegistrationString(
            "Invalid parameters used for creating a CM:" + registration_string
        )

    cm_id = registration_string_match.group("cm_id")
    raw_cm_info = registration_string_match.group("cm_info")
    try:
        cm_info = json.loads(raw_cm_info)
    except json.JSONDecodeError:
        raise InvalidRegistrationString(
            "Invalid task_info property when creating a CM:"
            + raw_cm_info
            + " for cm "
            + cm_id
        )
    return CalculationModule(cm_id, **cm_info)
