#!/usr/bin/env python3
import BaseCM.cm_base as cm_base
import BaseCM.cm_input as cm_input
from cm import processing

app = cm_base.get_default_app("heat_demand")
schema_path = cm_base.get_default_schema_path()


@app.task(base=cm_base.CMBase, bind=True, schema_path=schema_path)
def heat_demand(self, selection: dict, rasters: list, params: dict):
    if not rasters:
        raise ValueError("Raster list must be non-empty.")
    if "features" not in selection:
        raise ValueError("The selection must be a feature set.")
    if not selection["features"]:
        raise ValueError("The selection must be non-empty.")
    self.validate_params(params)

    raster = cm_input.get_raster_path(rasters[0])
    region = selection["features"][0]["geometry"]

    result = processing(raster=raster, region=region, parameters=params)

    return result


if __name__ == "__main__":
    cm_base.start_app(app)
