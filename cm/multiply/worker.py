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
def multiply_raster(selection: dict, rasters: list, params: dict):
    """This is a calculation module that multiplies the raster by an factor.
    If there is no raster, we raise a value error.
    If there are many rasters, we select the first one.
    """
    if not rasters:
        raise ValueError("Raster list must be non-empty.")
    if "features" not in selection:
        raise ValueError("The selection must be a feature set.")
    if not selection["features"]:
        raise ValueError("The selection must be non-empty.")
    raster_dir = os.path.join(os.environ["UPLOAD_DIR"], "raster")
    raster_path = os.path.join(raster_dir, rasters[0])
    factor = params["factor"]
    val_multiply = MultiplyRasterStats(selection, raster_path, factor)
    return val_multiply


if __name__ == "__main__":
    w = worker.WorkController(app=app)
    w.start()
