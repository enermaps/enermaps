#!/usr/bin/env python3
# from pprint import pprint
import geopandas as gpd
from BaseCM import cm_base as cm_base

from hddcdd import hdd_cdd_stats

app = cm_base.get_default_app("hddcdd")
schema_path = cm_base.get_default_schema_path()
input_layers_path = cm_base.get_default_input_layers_path()


@app.task(
    base=cm_base.CMBase,
    bind=True,
    schema_path=schema_path,
    input_layers_path=input_layers_path,
)
def hdd_cdd(self, selection: dict, rasters: list, params: dict):
    """This is a calculation module that multiplies the raster by an factor.
    If there is no raster, we raise a value error.
    If there are many rasters, we select the first one.
    """
    # logging.info("=" * 50)
    # logging.info("CM-HDD-CDD")
    # logging.info("Selection:")
    # logging.info(selection)
    # logging.info("Rasters:")
    # logging.info(rasters)
    # logging.info("Params:")
    # logging.info(params)
    features = selection["features"]
    if len(features) > 1:
        raise ValueError(
            "The CM support only one selection. "
            f"{len(features)} areas have been selected"
        )
    geo4326 = gpd.GeoDataFrame.from_features(features, crs="EPSG:4326").geometry

    self.validate_params(params)
    res = hdd_cdd_stats(
        geo=geo4326,
        refyear=params.get("reference year", 2050),
        rcp=params.get("scenario RCP", "historical"),
        t_base_h=params.get("base temperature for HDD", 18.0),
        t_base_c=params.get("base temperature for CDD", 22.0),
    )
    # logging.info(res)
    return res


if __name__ == "__main__":
    cm_base.start_app(app)
