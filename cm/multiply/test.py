import json
import os
import unittest

from rasterstats import zonal_stats

from multiply_raster import MultiplyRasterStats


class TestCM(unittest.TestCase):
    def test_multiply_raster_stats(self):
        """Testing to multiply the raster by a factor."""

        def get_testdata_path(filename):
            """Return the absolute path of the filename.
            """
            #current_file_dir = os.path.dirname(os.path.abspath(os.getcwd()))
            #testdata_dir = os.path.join(os.path.dirname(current_file_dir), "testdata")
            #print('path')
            #print(os.getcwd())
            #print(os.path.abspath(os.getcwd()))
            #print(os.path.join(testdata_dir, filename))
            os.path.join('.', 'testdata', filename)
            return os.path.join('.', 'testdata', filename)

        factor = 2
        selection_path = get_testdata_path("switzerland.geojson")
        raster = get_testdata_path("GeoTIFF_test.tif")
        #selection_path = os.path.join('.', 'testdata', filemane)
        with open(selection_path) as fd:
            selection = json.load(fd)
        val_double = MultiplyRasterStats(selection, raster, factor)
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
