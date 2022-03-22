#!/usr/bin/env python3

from BaseCM import cm_base as cm_base
from BaseCM import cm_input as cm_input

from multiply_raster import rasterstats

app = cm_base.get_default_app("multiply")
schema_path = cm_base.get_default_schema_path()
input_layers_path = cm_base.get_default_input_layers_path()
wiki = "https://enermaps-wiki.herokuapp.com/en/Home"


@app.task(
    base=cm_base.CMBase,
    bind=True,
    schema_path=schema_path,
    input_layers_path=input_layers_path,
    wiki=wiki,
)
def cm_multiply_raster(self, selection: dict, rasters: list, params: dict):
    """This is a calculation module that multiplies the raster by an factor.
    If there is no raster, we raise a value error.
    If there are many rasters, we select the first one.
    """
    if not rasters:
        raise ValueError("Raster list must be non-empty.")
    if "features" not in selection:
        raise ValueError("The selection must be a feature set.")
    if not selection["features"]:
        raise ValueError("The selection must be non-empty.")
    raster_path = cm_input.get_raster_path(rasters[0])
    selection_valid, invalid_selection_response = cm_input.validate_selection(
        selection=selection, raster=raster_path
    )
    if selection_valid is True:
        self.validate_params(params)
        factor = params["factor"]
        val_multiply = rasterstats(selection, raster_path, factor)
        return val_multiply
    else:
        return invalid_selection_response


if __name__ == "__main__":
    cm_base.start_app(app)
