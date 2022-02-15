#!/usr/bin/env python3

import BaseCM.cm_base as cm_base
import BaseCM.cm_input as cm_input

from calculation_module import res_calculation
from initialize import Param, Out_File_Path

app = cm_base.get_default_app("DHexpPot")
schema_path = cm_base.get_default_schema_path()
input_layers_path = cm_base.get_default_input_layers_path()


@app.task(
    base=cm_base.CMBase,
    bind=True,
    schema_path=schema_path,
    input_layers_path=input_layers_path,
)
def DHexpPot(self, selection: dict, rasters: list, params: dict):
    """This calculation module calculates the DH potentials.
    If there is no raster, we raise a value error.
    If there are many rasters, we select the first one.
    """
    if not rasters:
        raise ValueError("Raster list must be non-empty.")
    if "features" not in selection:
        raise ValueError("The selection must be a feature set.")
    if not selection["features"]:
        raise ValueError("The selection must be non-empty.")
    self.validate_params(params)

    for raster_file in rasters:
        raster = cm_input.get_raster_path(raster_file)
        name, extension = splitext(raster)
        if not isfile(raster) or extension.lower() not in [".tif", ".tiff"]:
            raise TypeError(f"The file path is not correct: {raster}")

    region = cm_input.merged_polygons(selection=selection)
    result = res_calculation(region=region, inRasterHDM_large=rasters[0], inRasterGFA_large=rasters[1], parameters=params)
    return result


if __name__ == "__main__":
    cm_base.start_app(app)
