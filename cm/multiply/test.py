import json
import os
import unittest

from rasterstats import zonal_stats

from multiply_raster import rasterstats


def get_testdata_path(filename):
    """Return the absolute path of the filename."""
    os.path.join('.', 'testdata', filename)
    return os.path.join('.', 'testdata', filename)


class TestCM(unittest.TestCase):



    def test_rasterstats(self):

    #def test_multiply_raster_stats(self):
    #    """Testing to multiply the raster by a factor."""

        factor = 2
        selection = get_testdata_path("selection_GeoTIFF.geojson")
        #selection = get_testdata_path("switzerland_bbox.geojson")
        raster = get_testdata_path("GeoTIFF_test.tif")
        #with open(selection_path) as fd:
            #selection = json.load(fd)
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

    def test_zonal_stats_switzerlandbbox(self):

        selection = get_testdata_path("switzerland_bbox.geojson")
        raster = get_testdata_path("GeoTIFF_test.tif")
        stats = zonal_stats(
            selection,
            raster,
            stats="count min mean max",
        )
        for key, value in stats[0].items():
            self.assertIsNotNone(value)


    def test_zonal_stats(self):
        pass


if __name__ == "__main__":
    unittest.main()