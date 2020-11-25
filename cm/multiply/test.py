import json
import unittest

from rasterstats import zonal_stats

from multiply_raster import MultiplyRasterStats


class TestCM(unittest.TestCase):
    def test_multiply_raster_stats(self):
        """Testing to multiply the raster by a factor."""
        factor = 2
        test_geojson = "selection_shapefile.geojson"
        with open(test_geojson) as fd:
            selection = json.load(fd)
        val_double = MultiplyRasterStats(
            selection, "GeoTIFF_test.tif", factor
        )
        stats = zonal_stats(
            test_geojson,
            "GeoTIFF_test.tif",
            stats="count min mean max",
        )
        for key, value in stats[0].items():
            if key != "count":
                self.assertAlmostEqual(
                    val_double[0][key], stats[0][key] * factor, places=4
                )


if __name__ == "__main__":
    unittest.main()
