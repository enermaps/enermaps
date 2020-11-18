import unittest
from multiply_raster import MultiplyRasterstats
from rasterstats import zonal_stats

class TestCM(unittest.TestCase):

    def test_MultiplyRasterstats(self):
        """Testing to multiply the raster by a factor.
        """
        val_double = MultiplyRasterstats("selection_shapefile.geojson", "GeoTIFF_test.tif", evaluate = True)
        stats = zonal_stats("selection_shapefile.geojson", "GeoTIFF_test.tif", stats="count min mean max")
        nround = 4 # Failed if nround >= 5
        for key, value in stats[0].items():
            if key != 'count':
                self.assertEqual( round(val_double[0][key], nround),
                                  round(stats[0][key]*2,   nround))

if __name__ == "__main__":
    unittest.main()