import json
import os
import unittest

from rasterstats import zonal_stats

from multiply_raster import rasterstats


class TestCM(unittest.TestCase):
    def test_rasterstats(self):
        """Testing to multiply the raster by a factor."""

        def get_testdata_path(filename):
            """Return the absolute path of the filename."""
            os.path.join('.', 'testdata', filename)
            return os.path.join('.', 'testdata', filename)

        factor = 2
        selection_path = get_testdata_path("selection_GeoTIFF.geojson")
        raster = get_testdata_path("GeoTIFF_test.tif")
        with open(selection_path) as fd:
            selection = json.load(fd)
        val_double = rasterstats(selection, raster, factor)
        stats = zonal_stats(
            selection,
            raster,
            stats="count min mean max",
        )
        for key, value in stats[0].items():
            if key != "count":
                self.assertAlmostEqual(
                    val_double[0][key], stats[0][key] * factor, places=4
                )


if __name__ == "__main__":
    unittest.main()
