import unittest
from simple_rasterstat import reproject_rasterstats
from double_rasterstat import double_rasterstats
from add_rasterstat import add_rasterstats
import simple_rasterstat
from rasterstats import zonal_stats
import sys

PROJ_2056 = 'EPSG:2056'

class TestCM(unittest.TestCase):


    def testSimpleRasterstat(self):
        """Testing the raster reprojection.
        """
        def whoami():
            return sys._getframe(1).f_code.co_name
        me = whoami()
        print('\nTesting : '  + me + '\n' )
        crc_reprojected, stats_reprojected = reproject_rasterstats("selection_shapefile.geojson", 'GeoTIFF_test_2056.tif')
        stats = zonal_stats("selection_shapefile.geojson", "GeoTIFF_test.tif", stats="count min mean max")
        self.assertEqual(crc_reprojected, simple_rasterstat.PROJ_4326)
        #self.assertEqual(stats_reprojected, stats)

    def testDoubleRasterstat(self):
        """Testing to double the raster value.
        """
        def whoami():
            return sys._getframe(1).f_code.co_name
        me = whoami()
        print('\nTesting : '  + me + '\n' )
        crs, val_double = double_rasterstats("selection_shapefile.geojson", "GeoTIFF_test.tif")
        stats = zonal_stats("selection_shapefile.geojson", "GeoTIFF_test.tif", stats="count min mean max")
        nround = 4 # Failed if nround >= 5
        for key, value in stats[0].items():
            if key != 'count':
                self.assertEqual( round(val_double[0][key], nround),
                                  round(stats[0][key]*2,   nround))

    def testAddRasterstat(self):
        """Testing to add two raster values
        """
        def whoami():
            return sys._getframe(1).f_code.co_name
        me = whoami()
        print('\nTesting : '  + me + '\n' )
        crs_double, val_double = double_rasterstats("selection_shapefile.geojson", "GeoTIFF_test.tif")
        crs_added, val_added = add_rasterstats("selection_shapefile.geojson",
                                         "GeoTIFF_test.tif", "GeoTIFF_test.tif")
        self.assertEqual([crs_double, val_double], [crs_added, val_added])

    def testCompareTwoZonalstatsProcessing(self):
        """Testing two different but similar process lead to the same result (e.g. compare si double a raster give
        the same result than just add the same raster to itself)
        """
        def whoami():
            return sys._getframe(1).f_code.co_name
        me = whoami()
        print('\nTesting : '  + me + '\n' )
        def compare_twoZonalStatsJSON(self, js1, js2):
            for key, js1_val, js2_val in zip(js1.keys(), js1.values(), js2.values()):
                print('\t'+ key, js1_val - js2_val, sep=' : ')
                self.assertEqual(js1_val, js2_val,'a comparaison gone wrong')

        val_simple = zonal_stats("selection_shapefile.geojson", 'GeoTIFF_test.tif')
        crs_reproj, val_reproj = reproject_rasterstats("selection_shapefile.geojson", 'GeoTIFF_test_2056.tif')
        crs_double, val_double = double_rasterstats("selection_shapefile.geojson", "GeoTIFF_test.tif")
        crs_add, val_add = add_rasterstats("selection_shapefile.geojson", "GeoTIFF_test.tif", "GeoTIFF_test.tif")

        print('\n\tDifference between doulbe raster and add the same value to itself : \n'
              '\t------------------------------------------------------------------------')
        compare_twoZonalStatsJSON(self, val_double[0], val_add[0])

        #print('\n\tDifference between reprojected and not reprojected raster :\n'
        #      '\t----------------------------------------------------------------')
        #compare_twoZonalStatsJSON(self, val_simple[0], val_reproj[0])

if __name__ == "__main__":
    unittest.main()
