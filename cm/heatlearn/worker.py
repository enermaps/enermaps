#!/usr/bin/env python3
from BaseCM import cm_base as cm_base
from BaseCM import cm_input as cm_input

from heatlearn import heatlearn

app = cm_base.get_default_app()
schema_path = cm_base.get_default_schema_path()


@app.task(base=cm_base.CMBase, bind=True, schema_path=schema_path)
def heat_learn(self, selection: dict, rasters: list, params: dict):
    """This is a calculation module that multiplies the raster by an factor.
    If there is no raster, we raise a value error.
    """
    # def create_data_indicator_str(json_form):
    #    for
    #    return data_indicator

    if not rasters:
        raise ValueError("Raster list must be non-empty.")
    if "features" not in selection:
        raise ValueError("The selection must be a feature set.")
    if not selection["features"]:
        raise ValueError("The selection must be non-empty.")
    raster_paths = cm_input.get_raster_path(rasters[0])
    self.validate_params(params)
    tile_size = params["tile_size"]
    results = heatlearn(selection, raster_paths, tile_size)
    return results


if __name__ == "__main__":
    cm_base.start_app(app)