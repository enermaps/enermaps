#!/usr/bin/env python3
# from pprint import pprint
from BaseCM import cm_base as cm_base
from BaseCM import cm_input as cm_input

import buildingload

# from BaseCM import cm_input as cm_input
app = cm_base.get_default_app("buildingload")
schema_path = cm_base.get_default_schema_path()
input_layers_path = cm_base.get_default_input_layers_path()


@app.task(
    base=cm_base.CMBase,
    bind=True,
    schema_path=schema_path,
    input_layers_path=input_layers_path,
)
def buildingload(self, selection: dict, rasters: list, params: dict):
    """This is a calculation module that simulates a building's space heating and cooling demand.
    If there is no raster, we raise a value error.
    If there are many rasters, we select the first one.
    """
    # Validate the raster used
    if not rasters:
        raise ValueError("Raster list must be non-empty.")
    # Validate the selection used
    if "features" not in selection:
        raise ValueError("The selection must be a feature set.")
    if not selection["features"]:
        raise ValueError("The selection must be non-empty.")
    # Validate the parameters used
    self.validate_params(params)

    res = buildingload(
        task = self,
        geojson = selection,   
        gfa_external = params.get("gross floor area", 100.0),
        n_stories = params.get("number of stories", 1),
        building_type = params.get("building type"),
        construction_year = params.get("construction year", 2020),
        t_set_min = params.get("set temperature for heating", 20.0),
        t_set_max = params.get("set temperature for cooling", 26.0),
        user_month = params.get("month"),
        user_week = params.get("week"),
        user_day = params.get("day"),
        user_model_length = params.get("model length"),
        roof_type_orientation = params.get("roof type and orientation"),
        user_roof_pitch = params.get("roof pitch", 30.0),
        w_f_r = params.get("wall to floor ratio", 1.3),
        L = params.get("building ratio length", 1),
        W = params.get("building ratio width", 1),
        facade_orientation = params.get("facade orientation"),
        a_door_1 = params.get("area of door", 2.0),
        window_front_proportion = params.get("area of front-facing windows", 10.0),
        window_back_proportion = params.get("area of rear-facing windows", 25.0),
        window_side_1_proportion = params.get("area of side 1 windows", 25.0),
        window_side_2_proportion = params.get("area of side 2 windows", 25.0)
    )
    return res


if __name__ == "__main__":
    cm_base.start_app(app)