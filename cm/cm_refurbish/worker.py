#!/usr/bin/env python3
from pprint import pprint

from BaseCM import cm_base as cm_base

from refurbish import ref_rate

# from BaseCM import cm_input as cm_input


app = cm_base.get_default_app("multiply")
schema_path = cm_base.get_default_schema_path()


@app.task(base=cm_base.CMBase, bind=True, schema_path=schema_path)
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

    # self.validate_params(params)
    return ref_rate()


if __name__ == "__main__":
    cm_base.start_app(app)
