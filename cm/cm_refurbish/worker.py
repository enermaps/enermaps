#!/usr/bin/env python3
from pprint import pprint

from BaseCM import cm_base as cm_base
from refurbish import ref_rate

# from BaseCM import cm_input as cm_input


app = cm_base.get_default_app("refurbish")
schema_path = cm_base.get_default_schema_path()
input_layers_path = cm_base.get_default_input_layers_path()


@app.task(
    base=cm_base.CMBase,
    bind=True,
    schema_path=schema_path,
    input_layers_path=input_layers_path,
)
def cm_refurbish_rate(self, selection: dict, rasters: list, params: dict):
    """This is a calculation module that multiplies the raster by an factor.
    If there is no raster, we raise a value error.
    If there are many rasters, we select the first one.
    """
    print("=" * 50)
    print("CM-HDD-CDD")
    print("Selection:")
    pprint(selection)
    print("Rasters:")
    pprint(rasters)
    print("Params:")
    pprint(params)

    self.validate_params(params)
    return ref_rate(
        geojson=selection,
        bstype=params.get("building typology", "Appartment blocks"),
        start_year=params.get("start epoch of construction", 1960),
        end_year=params.get("end epoch of construction", 1969),
        perc_basic=params.get("percentage basic refurbish rate", 10.0),
        perc_advance=params.get("percentage advance refurbish rate", 5.0),
        refyear=params.get("reference year", 2050),
        rcp=params.get("scenario RCP", "historical"),
        t_base_h=params.get("base temperature for HDD", 18.0),
        t_base_c=params.get("base temperature for CDD", 22.0),
    )


if __name__ == "__main__":
    cm_base.start_app(app)
