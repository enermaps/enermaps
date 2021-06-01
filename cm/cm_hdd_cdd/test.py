import json
import os
import unittest

# from hddcdd import hdd_cdd_stats

CURRENT_FILE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_testdata_path(filename):
    """Return the absolute path of the filename."""
    return os.path.join(CURRENT_FILE_DIR, "testdata", filename)


def load_geojson(test_filename):
    test_geojson = get_testdata_path(test_filename)
    with open(test_geojson) as fd:
        return json.load(fd)


class TestCM(unittest.TestCase):
    def test_hdd_cdd_stats(self):
        ...


if __name__ == "__main__":
    unittest.main()
