import json
import os
import unittest
import rasterio
import pyproj
print(os.environ)
print(os.listdir("/usr/local/lib/python3.8/dist-packages/rasterio/gdal_data/"))
os.environ['PROJ_LIB'] = '/usr/local/share/proj'
# os.environ["GDAL_DATA"] = "/usr/local/lib/python3.8/dist-packages/rasterio/gdal_data/"
# print(os.listdir("/usr/local/lib/python3.8/dist-packages/rasterio/gdal_data/"))

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
        raster = get_testdata_path("small_test.tif")
        stats = rasterstats(selection, raster, base_factor, stat_types=stat_types)
        double_stats = rasterstats(
            selection, raster, base_factor * multiplicator, stat_types=stat_types
        )
        self.assertCountEqual(
            stats["values"],
            stat_types,
            "Rasterstat request with two"
            " statistics returned more than two statistics",
        )
        self.assertCountEqual(
            double_stats["values"],
            stat_types,
            "Rasterstat request with two"
            " statistics returned more than two statistics",
        )
        double_values = double_stats["values"]
        unity_values = stats["values"]
        for stat_type in unity_values.keys():
            self.assertIn(stat_type, double_values)
            self.assertIn(stat_type, unity_values)
            self.assertAlmostEqual(
                unity_values[stat_type] * multiplicator,
                double_values[stat_type],
                places=4,
            )

    def test_mutliplefeature(self):
        selection = load_geojson("feature_collection.geojson")
        raster = get_testdata_path("small_test.tif")
        rasterstats(selection, raster, 1)

    def test_zonal_stats_switzerlandbbox(self):
        selection = load_geojson("switzerland_bbox.geojson")
        raster = get_testdata_path("big_test.tif")
        stats = rasterstats(selection, raster, 1)
        for key, value in stats.items():
            self.assertIsNotNone(value)


if __name__ == "__main__":
    unittest.main()
