import json
import unittest
from os import remove
from os.path import abspath, dirname, exists, isdir, isfile, join

import numpy as np

from .geofile import (
    RasterNotOverlappedError,
    clip_raster,
    get_projection,
    read_raster,
    write_raster,
)
from .settings import TESTDATA_DIR


class TestGeofileTools(unittest.TestCase):
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
        self.assertIsInstance(array1, np.ndarray)
        self.assertIsInstance(array2, np.ndarray)
        is_equal = np.equal(array1, array1).all()
        return is_equal

    def tuple_comparison(self, tuple1: tuple, tuple2: tuple):
        self.assertIsInstance(tuple1, tuple)
        self.assertIsInstance(tuple2, tuple)
        is_equal = tuple1 == tuple2
        return is_equal

    def get_shapes(self, region):
        with open(region) as file:
            shapes = json.load(file)
        self.assertIsInstance(shapes, dict, msg="Not a dictionary")
        return shapes

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

    def test_projection_getting(self):
        projection = get_projection(self.raster)
        is_valid = projection.is_valid
        self.assertTrue(is_valid)
        file_epsg_code = 4326
        self.assertEqual(projection.to_epsg(), file_epsg_code)

    def test_clipping_raster(self):
        shapes = self.get_shapes(self.region)
        clip_raster(src=self.raster, shapes=shapes, dst=self.dst)
        self.assertTrue(isfile(self.dst), msg=f"File not created: {self.dst}")

    def test_clipping_disjointed_raster(self):
        shapes = self.get_shapes(self.disjointed_region)
        with self.assertRaises(RasterNotOverlappedError):
            clip_raster(src=self.raster, shapes=shapes, dst=self.dst)

    def test_clipping_intercepted_raster(self):
        shapes = self.get_shapes(self.intercepted_region)
        clip_raster(src=self.raster, shapes=shapes, dst=self.dst)
        raster_map = read_raster(self.raster, return_geo_transform=False)
        dst_map = read_raster(self.dst, return_geo_transform=False)
        self.assertGreaterEqual(np.mean(raster_map), np.mean(dst_map))

    def test_read_raster(self):
        map_array, geotransform = read_raster(raster=self.raster)
        self.assertIsInstance(map_array, np.ndarray)
        self.assertIsInstance(geotransform, tuple)

    def test_write_raster(self):
        map_array, geotransform = read_raster(raster=self.raster)
        projection = get_projection(geofile=self.raster)
        write_raster(
            map_array=map_array,
            projection=projection,
            geotransform=geotransform,
            dst=self.dst,
        )
        dst_map_array, dst_geotransform = read_raster(raster=self.raster)
        self.comparator(map_array, dst_map_array, comparison=self.array_comparison)
        self.comparator(
            geotransform, dst_geotransform, comparison=self.tuple_comparison
        )

    def tearDown(self):
        if exists(self.dst):
            remove(self.dst)


if __name__ == "__main__":
    unittest.main()
