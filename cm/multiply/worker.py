#!/usr/bin/env python3
import inspect
import json

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
        with open("schema.json") as f:
            self.schema = json.load(f)
        raw_name = self.__wrapped__.__name__
        spaced_name = raw_name.replace('_', ' ').replace('-', ' ')
        self.name = spaced_name.capitalize()



    @property
    def cm_info(self):
        d = {}
        d["parameters"] = self.parameters
        d["schema"] = self.schema
        d["doc"] = self.__doc__
        d["name"] = self.name
        return json.dumps(d)


@app.task(base=BaseTask)
def multiply_raster(path_selection, path_tif, params):
    """This is a calculation module that multiplies the raster by an factor."""
    factor = params["factor"]
    val_multiply = MultiplyRasterStats(path_selection, path_tif, factor)
    return val_multiply


if __name__ == "__main__":
    w = worker.WorkController(app=app)
    w.start()
