#!/usr/bin/env python3
import geopandas as gpd
from BaseCM import cm_base as cm_base

from refurbish import ref_rate

# from BaseCM import cm_input as cm_input


app = cm_base.get_default_app("refurbish")
schema_path = cm_base.get_default_schema_path()
input_layers_path = cm_base.get_default_input_layers_path()
wiki = "https://enermaps-wiki.herokuapp.com/en/Refurbish.md"


@app.task(
    base=cm_base.CMBase,
    bind=True,
    schema_path=schema_path,
    input_layers_path=input_layers_path,
    wiki=wiki,
)
def refurbish_rate(self, selection: dict, rasters: list, params: dict):
    """This is a calculation module compute the centroid
    of the selected region and query a set of rasters with the
    Heating and Cooling Degree Days computed from the CORDEX
    dataset, then assess the heating and cooling demand for the
    selected region combining building characteristics from the
    TABULA dataset.
    CM support only a single feature selection, in case of
    multiple selection it raise an error.
    """
    features = selection["features"]
    if len(features) > 1:
        raise ValueError(
            "The CM support only one selection. "
            f"{len(features)} areas have been selected"
        )
    geo4326 = gpd.GeoDataFrame.from_features(features, crs="EPSG:4326").geometry

    self.validate_params(params)
    res = ref_rate(
        geo=geo4326,
        bstype=params.get("building typology", "Appartment blocks"),
        start_year=params.get("start epoch of construction", 1960),
        end_year=params.get("end epoch of construction", 1969),
        perc_basic=params.get("percentage basic refurbish rate", 10.0),
        perc_advance=params.get("percentage advance refurbish rate", 5.0),
        refyear=params.get("reference year", 2050),
        rcp=params.get("scenario RCP", "historical"),
        t_base_h=params.get("base temperature for HDD", 15.0),
        t_base_c=params.get("base temperature for CDD", 24.0),
    )
    return res


if __name__ == "__main__":
    cm_base.start_app(app)
