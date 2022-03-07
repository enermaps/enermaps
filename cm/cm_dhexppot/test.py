import json
import os

# import unittest
from calculation_module import res_calculation

CURRENT_FILE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_testdata_path(filename):
    """Return the absolute path of the filename."""
    return os.path.join(CURRENT_FILE_DIR, "testdata", filename)


def load_geojson(test_filename):
    test_geojson = get_testdata_path(test_filename)
    with open(test_geojson) as fd:
        return json.load(fd)


def createParams(use_default_cost_factors):
    params = dict()
    params["scenario"] = "Test scenario"
    params["country"] = "AT"
    params["distribution_grid_cost_ceiling"] = 20
    # pixel threshold may not be changed. 20 is the correct value.
    params["pix_threshold"] = 35
    params["DH_threshold"] = 5
    params["start_year"] = 2022
    params["last_year"] = 2035
    params["st_dh_connection_rate"] = 30
    params["end_dh_connection_rate"] = 50
    params["depreciation_period"] = 40
    params["interest"] = 0.02
    params["use_default_cost_factors"] = use_default_cost_factors
    params["c1"] = 349
    params["c2"] = 4213
    return params


# class TestCM(unittest.TestCase):

# def test_dhexppot(self, getHDD_function):
def test_dhexppot():
    selection = load_geojson("wien_sued.geojson")
    hdm_raster_paths = get_testdata_path("test_hdm_vienna.tif")
    gfa_raster_paths = get_testdata_path("test_gfa_vienna.tif")
    params = createParams(True)
    res_calculation(selection, hdm_raster_paths, gfa_raster_paths, params, task=None, not_test_mode=False)
    """
    params = createParams(False)
    res_test_2 = res_calculation(selection: dict, hdm_raster_paths, gfa_raster_paths, params)

    print(stats["values"]["maxDHdem [GWh]"], flush=True)
    self.assertEqual(
        stats["values"]["maxDHdem [GWh]"],
        468,  # with full grid
        "Request expecting 0 returned different values",
    )

    self.assertEqual(task.nb_rasters_posted, 1)
    """


if __name__ == "__main__":
    # unittest.main()
    test_dhexppot()
