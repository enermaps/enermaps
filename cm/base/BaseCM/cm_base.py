#!/usr/bin/env python3
"""Base module for the calculation modules.
"""
import inspect
import json
import logging
import os

import jsonschema
from celery import Celery, Task
from celery.worker import worker

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND")


def get_default_app(name):
    """Create default Celery application."""
    app = Celery(name, broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

    app.conf.update(
        task_serializer="json",
        accept_content=["json"],  # Ignore other content
        result_serializer="json",
        timezone="Europe/Zurich",
        enable_utc=True,
        task_default_queue=name,
    )
    return app


def get_default_schema_path():
    """return the schema.json relative to the caller.
    We expect to find the schema.json file in the same directory as the worker.
    """
    filename = inspect.stack()[1].filename
    dir_path = os.path.dirname(os.path.abspath(filename))
    schema_path = os.path.join(dir_path, "schema.json")
    if not os.path.isfile(schema_path):
        raise FileNotFoundError(
            "Cannot find schema.json file under the path " + schema_path
        )
    return schema_path


class CMBase(Task):
    schema_path = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = self.app.conf.task_default_queue
        signature = inspect.signature(self.__wrapped__)
        self.parameters = [p for p in signature.parameters]
        self.pretty_name = CMBase.format_function(self.__wrapped__)
        if self.schema_path:
            with open(self.schema_path) as fd:
                self.schema = json.load(fd)
        else:
            self.schema = {}

    @staticmethod
    def format_function(function):
        """From a named callable  extract its name then
        format it to be human readable.
        """
        raw_name = function.__name__
        spaced_name = raw_name.replace("_", " ").replace("-", " ")
        return spaced_name.capitalize()

    def validate_params(self, params):
        """Validate the dict parameters based on the schema.json declaration.
        Raises a ValueError containing the declaration of the validation failure.
        """
        try:
            jsonschema.validate(params, schema=self.schema)
        except jsonschema.ValidationError as err:
            raise ValueError(str(err))

    @property
    def cm_info(self):
        """Return worker information formatted as a json string"""
        d = {}
        d["parameters"] = self.parameters
        d["schema"] = self.schema
        d["doc"] = self.__doc__
        d["pretty_name"] = self.pretty_name
        d["name"] = self.name
        d["queue"] = self.queue
        return json.dumps(d)


def base_task(app, schema_path):
    """Wrapper for the app.task decoration"""
    return app.task(base=CMBase, bind=True, schema_path=schema_path, queue=app.name)


def start_app(app):
    """Start the celery application passed as single parameter"""
    logging.basicConfig(level=logging.ERROR)
    w = worker.WorkController(app=app)
    w.start()
