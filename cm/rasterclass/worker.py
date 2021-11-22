#!/usr/bin/env python3

import geopandas as gpd
import numpy as np
import rasterio
import rasterio.mask
from BaseCM import cm_base as cm_base
from BaseCM import cm_input as cm_input
from BaseCM.cm_output import validate

app = cm_base.get_default_app("rasterclass")
schema_path = cm_base.get_default_schema_path()
input_layers_path = cm_base.get_default_input_layers_path()


@app.task(
    base=cm_base.CMBase,
    bind=True,
    schema_path=schema_path,
    input_layers_path=input_layers_path,
)
def cm_rasterclass(self, selection: dict, rasters: list, params: dict):
    ret = dict()
    ret["graphs"] = {}
    ret["geofiles"] = {}
    ret["values"] = {}
    ret["warnings"] = {}

    if len(rasters) > 0:
        raster_path = cm_input.get_raster_path(rasters[0])  # EPSG:3035
        shapes = gpd.GeoDataFrame.from_features(selection["features"], crs="EPSG:4326")
        shapes = shapes.to_crs("EPSG:3035").geometry

        with rasterio.open(raster_path) as src:
            i, t = rasterio.mask.mask(src, shapes, crop=True)
            ratio = np.sum(i[i == params["class"]]) / np.sum(i[i >= 0])
            ret["values"] = {"ratio": np.round(ratio, 2)}

    return validate(ret)


if __name__ == "__main__":
    cm_base.start_app(app)
