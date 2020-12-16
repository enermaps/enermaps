#!/usr/bin/env python3
"""Base module for the calculation modules.
"""
import inspect
import json

import jsonschema
from celery import Celery, Task
from celery.worker import worker


def get_default_app():
    app = Celery(__name__, broker="redis://redis//", backend="redis://redis")

    app.conf.update(
        task_serializer="json",
        accept_content=["json"],  # Ignore other content
        result_serializer="json",
        timezone="Europe/Zurich",
        enable_utc=True,
    )
    return app


class CMBase(Task):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        signature = inspect.signature(self.__wrapped__)
        self.parameters = [p for p in signature.parameters]
        self.pretty_name = CMBase.format_function(self.__wrapped__)

    def __call__(self, *args, **kwargs):
        with open(self.schema_path) as fd:
            # verify that we have a valid json schema
            self.schema = json.load(fd)

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
        return json.dumps(d)


def base_task(app, schema_path):
    """Wrapper for the app.task decoration"""
    return app.task(base=CMBase, bind=True, schema_path=schema_path)


def start_app(app):
    """Start the celery application passed as single parameter"""
    w = worker.WorkController(app=app)
    w.start()
