import json
import os
import unittest

from heatlearn import heatlearn

CURRENT_FILE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_testdata_path(filename):
    """Return the absolute path of the filename."""
    return os.path.join(CURRENT_FILE_DIR, "testdata", filename)


def load_geojson(test_filename):
    test_geojson = get_testdata_path(test_filename)
    with open(test_geojson) as fd:
        return json.load(fd)


class TestCM(unittest.TestCase):
    def test_rasterstats(self):
        selection = load_geojson("selection_esm.geojson")
        raster = get_testdata_path("2859.tif")
        stats = heatlearn(selection, raster, 500)

        self.assertEqual(
            stats["values"]["results"],
            26000.25,
            "Request especting 0" " returned different values",
        )


if __name__ == "__main__":
    unittest.main()
