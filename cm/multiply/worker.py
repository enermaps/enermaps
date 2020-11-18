import json
import inspect
import marshmallow
from celery import Celery, Task
from multiply_raster import MultiplyRasterstats
import IPython

app = Celery(__name__, broker="redis://guest@localhost//", backend="redis://localhost")

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

# used CMSchema is the next step
class CMSchema(marshmallow.Schema):
    rasters = marshmallow.fields.List(marshmallow.fields.String)
    #this could be a bit more restrictive
    selection = marshmallow.fields.Mapping() #GEOJson
    scale_factor = marshmallow.fields.Integer()

@app.task(base=BaseTask)
def MultiplyRaster():
    """This is a calculation module that multiplies the raster by an factor.
    """
    val_multiply = MultiplyRasterstats("selection_shapefile.geojson", "GeoTIFF_test.tif",factor =3, evaluate = False)
    return val_multiply

if __name__ == "__main__":
    app.worker_main()
    #print(help(app))
    #import time
    #time.sleep(400)
    #IPython.embed()