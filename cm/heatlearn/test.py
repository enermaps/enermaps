import json
import os
import unittest

import heatlearn

CURRENT_FILE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_testdata_path(filename):
    """Return the absolute path of the filename."""
    return os.path.join(CURRENT_FILE_DIR, "testdata", filename)


def load_geojson(test_filename):
    test_geojson = get_testdata_path(test_filename)
    with open(test_geojson) as fd:
        return json.load(fd)


class MockTask:
    def __init__(self):
        self.nb_rasters_posted = 0

    def post_raster(self, raster_name, raster_fd):
        self.nb_rasters_posted += 1


class TestCM(unittest.TestCase):
    def test_rasterstats(self):
        selection = load_geojson("ge_rive_droite_500.geojson")
        raster_paths = [get_testdata_path("200km_2p5m_N26E38_07_18.tif")]

        task = MockTask()

        stats = heatlearn.heatlearn(task, selection, raster_paths, 500, 2020)
        print(stats["values"]["Annual heating demand [GWh]"], flush=True)
        self.assertEqual(
            stats["values"]["Annual heating demand [GWh]"],
            468,  # with full grid
            "Request expecting 0 returned different values",
        )

        self.assertEqual(task.nb_rasters_posted, 1)


if __name__ == "__main__":
    unittest.main()
