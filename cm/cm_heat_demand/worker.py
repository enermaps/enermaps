#!/usr/bin/env python3
from os.path import isfile, splitext

import BaseCM.cm_base as cm_base
import BaseCM.cm_input as cm_input

from heat_demand import processing

app = cm_base.get_default_app("heat_demand")
schema_path = cm_base.get_default_schema_path()


@app.task(base=cm_base.CMBase, bind=True, schema_path=schema_path, available_layer=[43])
def heat_demand(self, selection: dict, rasters: list, params: dict):
    if "features" not in selection:
        raise ValueError("The selection must be a feature set.")
    if not selection["features"]:
        raise ValueError("The selection must be non-empty.")
    self.validate_params(params)
    self.validate_layers(rasters=rasters)
    raster = cm_input.get_raster_path(rasters[0])
    name, extension = splitext(raster)
    if not isfile(raster) or extension.lower() not in [".tif", ".tiff"]:
        raise TypeError(f"The file path is not correct: {raster}")
    region = cm_input.merged_polygons(selection=selection)

    result = processing(task=self, raster=raster, region=region, parameters=params)

    return result


if __name__ == "__main__":
    cm_base.start_app(app)
