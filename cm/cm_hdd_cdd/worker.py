#!/usr/bin/env python3
# from pprint import pprint
from BaseCM import cm_base as cm_base

from hddcdd import hdd_cdd_stats

# from BaseCM import cm_input as cm_input


app = cm_base.get_default_app("hddcdd")
schema_path = cm_base.get_default_schema_path()


@app.task(base=cm_base.CMBase, bind=True, schema_path=schema_path)
def cm_hddcdd(self, selection: dict, rasters: list, params: dict):
    """This is a calculation module that multiplies the raster by an factor.
    If there is no raster, we raise a value error.
    If there are many rasters, we select the first one.
    """
    # print("=" * 50)
    # print("CM-HDD-CDD")
    # print("Selection:")
    # pprint(selection)
    # print("Rasters:")
    # pprint(rasters)
    # print("Params:")
    # pprint(params)

    # self.validate_params(params)
    res = hdd_cdd_stats(
        geojson=selection,
        refyear=params.get("reference year", 2050),
        rcp=params.get("scenario RCP", "historical"),
        t_base_h=params.get("base temperature for HDD", 18.0),
        t_base_c=params.get("base temperature for CDD", 22.0),
    )
    # pprint(res)
    return res


if __name__ == "__main__":
    cm_base.start_app(app)
