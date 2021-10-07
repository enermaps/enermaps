#!/usr/bin/env python3

import os

from BaseCM import cm_base as cm_base
from BaseCM import cm_input as cm_input

import heatlearn

ADMISSIBLE_TILE_SIZES = [500, 300]

app = cm_base.get_default_app("heatlearn")
schema_path = cm_base.get_default_schema_path()

api_base_url = os.environ.get("API_BASE_URL")


@app.task(base=cm_base.CMBase, bind=True, schema_path=schema_path)
def heat_learn(self, selection: dict, rasters: list, params: dict):
    """This is a calculation module that applies the HeatLearn model.
    If there is no raster, we raise a value error.
    """

    tile_size = params["tileSize"]
    year = params["year"]

    if not rasters:
        raise ValueError("Raster list must be non-empty.")
    if len(rasters) > 1:
        raise ValueError("Please select only one raster for now")
    if "features" not in selection:
        raise ValueError("The selection must be a feature set.")
    if not selection["features"]:
        raise ValueError("The selection must be non-empty.")

    if tile_size not in heatlearn.MODELS.keys():
        raise ValueError(
            "Only these tile sizes are possible: {}".format(
                ", ".join(heatlearn.MODELS.keys())
            )
        )

    raster_paths = []
    for raster in rasters:
        raster_paths.append(cm_input.get_raster_path(raster))
    self.validate_params(params)

    results = heatlearn.heatlearn(
        selection, raster_paths, tile_size, year, api_base_url
    )
    return results


if __name__ == "__main__":
    cm_base.start_app(app)
