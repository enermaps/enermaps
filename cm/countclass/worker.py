#!/usr/bin/env python3
import BaseCM.cm_base as cm_base
import BaseCM.cm_input as cm_input

from countclass import calculate

app = cm_base.get_default_app()
schema_path = cm_base.get_default_schema_path()


@app.task(base=cm_base.CMBase, bind=True, schema_path=schema_path)
def countclass(self, selection: dict, rasters: list, params: dict):
    """This is a calculation module that callculates the area of a given raster class.
    If there is no raster, we raise a value error.
    If there are many rasters, we select the first one.
    """

    if not rasters:
        raise ValueError("Raster list must be non-empty.")
    if "features" not in selection:
        raise ValueError("The selection must be a feature set.")
    if not selection["features"]:
        raise ValueError("The selection must be non-empty.")
    raster_path = cm_input.get_raster_path(rasters[0])
    self.validate_params(params)
    rasterclass = params["rasterclass"]
    results = calculate(selection, raster_path, rasterclass)

    ret = {}
    ret["graphs"] = {}
    ret["geofiles"] = {}
    ret["values"] = results

    return ret


if __name__ == "__main__":
    cm_base.start_app(app)
