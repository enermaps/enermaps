import json
import unittest
from os import remove
from os.path import abspath, dirname, exists, isdir, isfile, join

import numpy as np

from . import geofile
from .settings import TESTDATA_DIR


class TestGeofileTools(unittest.TestCase):
    def setUp(self):
        def is_file(*files: str):
            for file in files:
                self.assertTrue(isfile(file), msg=f"Not a file : {file}")

        self.raster = join(TESTDATA_DIR, "src.tif")
        self.region = join(TESTDATA_DIR, "region.json")
        self.disjointed_region = join(TESTDATA_DIR, "disjointed_region.json")
        self.intercepted_region = join(TESTDATA_DIR, "intercepted_region.json")
        is_file(
            self.raster, self.region, self.disjointed_region, self.intercepted_region
        )

        self.current_dir = dirname(abspath(__file__))
        self.assertTrue(
            isdir(self.current_dir), msg=f"Not a directory: {self.current_dir}"
        )

        self.dst = join(self.current_dir, "clipped_raster_test.tif")
        self.assertFalse(exists(self.dst), msg=f"File already exist: {self.dst}")

    def tearDown(self):
        if exists(self.dst):
            remove(self.dst)

    def comparator(self, *elements, comparison):
        for element in elements:
            reference = None
            if reference is None:
                reference = element
            is_equal = comparison(reference, element)
            self.assertTrue(is_equal)

    def array_comparison(
        self,
        array1: np.ndarray,
        array2: np.ndarray,
    ):
        """
        Compare two arrays.

        Inputs :
            * array1 : first array.
            * array2 : second array.

        Output :
            * boolean : True (if arrays are the same) or False.
        """
        self.assertIsInstance(array1, np.ndarray)
        self.assertIsInstance(array2, np.ndarray)
        is_equal = np.equal(array1, array1).all()
        return is_equal

    def tuple_comparison(self, tuple1: tuple, tuple2: tuple):
        """Compare two tuple.

        Inputs :
            * tuple1 : first tuple.
            * tuple2 : second tuple.

        Output :
            * boolean : True (if arrays are the same) or False.
        """
        self.assertIsInstance(tuple1, tuple)
        self.assertIsInstance(tuple2, tuple)
        is_equal = tuple1 == tuple2
        return is_equal

    def test_write_raster(self):
        """
        Copy a raster and read the copy as well as the original to make sure that
        both have the same geotransformation and the same map array.
        """
        map_array, geotransform = geofile.read_raster(raster=self.raster)
        projection = geofile.get_projection(geofile=self.raster)
        geofile.write_raster(
            map_array=map_array,
            projection=projection,
            geotransform=geotransform,
            dst=self.dst,
        )
        dst_map_array, dst_geotransform = geofile.read_raster(raster=self.raster)
        self.comparator(map_array, dst_map_array, comparison=self.array_comparison)
        self.comparator(
            geotransform, dst_geotransform, comparison=self.tuple_comparison
        )

    def get_shapes(self, region):
        """Try load a geojson into a Python dictionary."""
        with open(region) as file:
            shapes = json.load(file)
        self.assertIsInstance(shapes, dict, msg="Not a dictionary")
        return shapes

    def test_projection_getting(self):
        """
        Try to get a valid projection from a raster and check if
        this projection corresponding to an 'EPSG:4326' projection.
        """
        projection = geofile.get_projection(self.raster)
        is_valid = projection.is_valid
        self.assertTrue(is_valid)
        file_epsg_code = 4326
        self.assertEqual(projection.to_epsg(), file_epsg_code)

    def test_clipping_raster(self):
        """
        Try to clip a raster based on geojson shape
        and save the result.
        """
        shapes = self.get_shapes(self.region)
        geofile.clip_raster(src=self.raster, shapes=shapes, dst=self.dst)
        self.assertTrue(isfile(self.dst), msg=f"File not created: {self.dst}")

    def test_clipping_disjointed_raster(self):
        """
        Try to clip raster with region disjointed form the raster.
        """
        shapes = self.get_shapes(self.disjointed_region)
        with self.assertRaises(geofile.RasterNotOverlappedError):
            geofile.clip_raster(src=self.raster, shapes=shapes, dst=self.dst)

    def test_clipping_intercepted_raster(self):
        """Try to clip a raster with a region that intercepted the raster."""
        shapes = self.get_shapes(self.intercepted_region)
        geofile.clip_raster(src=self.raster, shapes=shapes, dst=self.dst)
        raster_map = geofile.read_raster(self.raster, return_geo_transform=False)
        dst_map = geofile.read_raster(self.dst, return_geo_transform=False)
        self.assertGreaterEqual(np.mean(raster_map), np.mean(dst_map))

    def test_read_raster(self):
        """
        Try to read a raster as a map array and return the geotransform.
        """
        map_array, geotransform = geofile.read_raster(raster=self.raster)
        self.assertIsInstance(map_array, np.ndarray)
        self.assertIsInstance(geotransform, tuple)


if __name__ == "__main__":
    unittest.main()
