import json
import os
import unittest

from multiply_raster import rasterstats

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
        stat_types = ("min", "max")
        base_factor = 1
        multiplicator = 2
        selection = load_geojson("selection_GeoTIFF.geojson")
        raster = get_testdata_path("GeoTIFF_test.tif")
        stats = rasterstats(selection, raster, base_factor, stat_types=stat_types)
        double_stats = rasterstats(
            selection, raster, base_factor * multiplicator, stat_types=stat_types
        )
        self.assertEqual(
            len(stats),
            1,
            "a selection with a single feature "
            "returned more stats than the number of feature.",
        )
        self.assertEqual(
            len(double_stats),
            1,
            "a selection with a single feature "
            "returned more stats than the number of feature.",
        )
        for stat in double_stats + stats:
            self.assertCountEqual(
                stat,
                stat_types,
                "Rasterstat request with two"
                " statistics returned more than two statistics",
            )
        for stat, double_stat in zip(stats, double_stats):
            for stat_type in stat.keys():
                self.assertIn(stat_type, stat)
                self.assertIn(stat_type, double_stat)
                self.assertAlmostEqual(
                    stat[stat_type] * multiplicator, double_stat[stat_type], places=4
                )

    def test_mutliplefeature(self):
        selection = load_geojson("feature_collection.geojson")
        raster = get_testdata_path("GeoTIFF_test.tif")
        rasterstats(selection, raster, 1)

    def test_zonal_stats_switzerlandbbox(self):
        selection = load_geojson("switzerland_bbox.geojson")
        raster = get_testdata_path("GeoTIFF_test.tif")
        stats = rasterstats(selection, raster, 1)
        for key, value in stats[0].items():
            self.assertIsNotNone(value)


if __name__ == "__main__":
    unittest.main()
