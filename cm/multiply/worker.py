#!/usr/bin/env python3
import inspect
import json
import os

from celery import Celery, Task
from celery.worker import worker

from multiply_raster import MultiplyRasterStats

app = Celery(__name__, broker="redis://redis//", backend="redis://redis")

app.conf.update(
    task_serializer="json",
    accept_content=["json"],  # Ignore other content
    result_serializer="json",
    timezone="Europe/Zurich",
    enable_utc=True,
)


class BaseTask(Task):
    def __init__(self, *args, **kwargs):
        super(BaseTask, self).__init__(*args, **kwargs)
        signature = inspect.signature(self.__wrapped__)
        self.parameters = [p for p in signature.parameters]
        self.pretty_name = BaseTask.format_function(self.__wrapped__)
        with open("schema.json") as fd:
            self.schema = json.load(fd)

    @staticmethod
    def format_function(function):
        """From a named callable  extract its name then
        format it to be human readable.
        """
        raw_name = function.__name__
        spaced_name = raw_name.replace("_", " ").replace("-", " ")
        return spaced_name.capitalize()

    @property
    def cm_info(self):
        d = {}
        d["parameters"] = self.parameters
        d["schema"] = self.schema
        d["doc"] = self.__doc__
        d["pretty_name"] = self.name
        return json.dumps(d)


@app.task(base=BaseTask)
def multiply_raster(selection, rasters, params):
    """This is a calculation module that multiplies the raster by an factor."""
    os.chdir(os.environ['UPLOAD_DIR'] + "/raster")
    factor = params["factor"]
    val_multiply = MultiplyRasterStats(selection, rasters, factor)
    return val_multiply


if __name__ == "__main__":
    w = worker.WorkController(app=app)
    w.start()
