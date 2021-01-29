import json
import os
import unittest

from countclass import calculate

CURRENT_FILE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_testdata_path(filename):
    """Return the absolute path of the filename."""
    return os.path.join(CURRENT_FILE_DIR, "testdata", filename)


def load_geojson(test_filename):
    test_geojson = get_testdata_path(test_filename)
    with open(test_geojson) as fd:
        return json.load(fd)


class TestCM(unittest.TestCase):
   def test1(self):
        rasterclass = 50
        selection = load_geojson("selection_esm.geojson")
        raster = get_testdata_path("esm.tif")
        res = calculate(selection, raster, rasterclass)
        self.assertAlmostEqual(
            res["values"][0],
            0.02,
            places=4,)


if __name__ == "__main__":
    unittest.main()
