import json
import inspect
import marshmallow
from celery import Celery, Task
from celery.worker import worker
#from multiply_raster import MultiplyRasterstats

app = Celery(__name__, broker="redis://redis//", backend="redis://redis")

app.conf.update(
    task_serializer="json",
    accept_content=["json"],  # Ignore other content
    result_serializer="json",
    timezone="Europe/Zurich",
    enable_utc=True,)

class BaseTask(Task):
    def __init__(self, *args, **kwargs):
        super(BaseTask, self).__init__(*args, **kwargs)
        signature = inspect.signature(self.__wrapped__)
        self.parameters = [p for p in signature.parameters]
        #self.schema = CMSSchema

    @property
    def cm_info(self):
        d = {}
        d["parameters"] = self.parameters
        d["schema"] = {}
        d["doc"] = self.__doc__
        return json.dumps(d)

@app.task(base=BaseTask)
def MultiplyRaster(path_selection, path_tif, factor):
    """This is a calculation module that multiplies the raster by an factor.
    """
    val_multiply = MultiplyRasterstats(path_selection, path_tif,factor)
    return val_multiply

if __name__ == "__main__":
    w = worker.WorkController(app=app)
    w.start()
