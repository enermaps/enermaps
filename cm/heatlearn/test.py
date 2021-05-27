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
        selection = load_geojson("ge_rive_droite_500.geojson")
        raster_paths = [get_testdata_path("200km_2p5m_N26E38_07_18.tif")]
        stats = heatlearn(selection, raster_paths, 500)

        self.assertEqual(
            stats["values"]["results"],
            167943,
            "Request especting 0" " returned different values",
        )


if __name__ == "__main__":
    unittest.main()
