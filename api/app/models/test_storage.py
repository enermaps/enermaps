import shutil
import tempfile

from app.common import path
from app.common.test import BaseApiTest
from app.models import storage

ENCODED_VAR = path.encode("var")


class TestCreate(BaseApiTest):
    def testArea(self):
        with self.flask_app.app_context():
            storage_instance = storage.create("area/NUTS42")
            self.assertTrue(storage_instance is not None)
            self.assertTrue(isinstance(storage_instance, storage.AreaStorage))

    def testRaster(self):
        with self.flask_app.app_context():
            storage_instance = storage.create("raster/42")
            self.assertTrue(storage_instance is not None)
            self.assertTrue(isinstance(storage_instance, storage.GeoDBRasterStorage))

    def testVector(self):
        with self.flask_app.app_context():
            storage_instance = storage.create("vector/42")
            self.assertTrue(storage_instance is not None)
            self.assertTrue(isinstance(storage_instance, storage.GeoDBVectorStorage))

    def testCMOutput(self):
        with self.flask_app.app_context():
            storage_instance = storage.create("cm/blah")
            self.assertTrue(storage_instance is not None)
            self.assertTrue(isinstance(storage_instance, storage.CMOutputStorage))

    def testUnknown(self):
        with self.flask_app.app_context():
            storage_instance = storage.create("unknown/blah")
            self.assertTrue(storage_instance is None)


class TestGeoDBRasterStorage(BaseApiTest):
    def testRootDir(self):
        with self.flask_app.app_context():
            storage_instance = storage.GeoDBRasterStorage()
            self.assertEquals(
                storage_instance.get_root_dir(), f"{self.geodb_cache_dir}/rasters"
            )

    def testTmpDir(self):
        with self.flask_app.app_context():
            storage_instance = storage.GeoDBRasterStorage()
            self.assertEquals(
                storage_instance.get_tmp_dir(), f"{self.geodb_cache_dir}/tmp"  # nosec
            )

    def testDir(self):
        with self.flask_app.app_context():
            storage_instance = storage.GeoDBRasterStorage()
            self.assertEquals(
                storage_instance.get_dir("raster/10"),
                f"{self.geodb_cache_dir}/rasters/10",
            )
            self.assertEquals(
                storage_instance.get_dir("raster/10/2015"),
                f"{self.geodb_cache_dir}/rasters/10/2015",
            )
            self.assertEquals(
                storage_instance.get_dir(f"raster/10/2015/{ENCODED_VAR}"),
                f"{self.geodb_cache_dir}/rasters/10/2015/{ENCODED_VAR}",
            )
            self.assertEquals(
                storage_instance.get_dir(f"raster/10//{ENCODED_VAR}"),
                f"{self.geodb_cache_dir}/rasters/10/{ENCODED_VAR}",
            )

    def testFilePath(self):
        with self.flask_app.app_context():
            storage_instance = storage.GeoDBRasterStorage()
            self.assertEquals(
                storage_instance.get_file_path("raster/10", "layer.tif"),
                f"{self.geodb_cache_dir}/rasters/10/layer.tif",
            )
            self.assertEquals(
                storage_instance.get_file_path("raster/10/2015", "layer.tif"),
                f"{self.geodb_cache_dir}/rasters/10/2015/layer.tif",
            )
            self.assertEquals(
                storage_instance.get_file_path(
                    f"raster/10/2015/{ENCODED_VAR}", "layer.tif"
                ),
                f"{self.geodb_cache_dir}/rasters/10/2015/{ENCODED_VAR}/layer.tif",
            )
            self.assertEquals(
                storage_instance.get_file_path(
                    f"raster/10//{ENCODED_VAR}", "layer.tif"
                ),
                f"{self.geodb_cache_dir}/rasters/10/{ENCODED_VAR}/layer.tif",
            )


class TestGeoDBRasterStorageWithoutCache(BaseApiTest):
    def setUp(self):
        super().setUp()
        self.geodb_dir = tempfile.mkdtemp()
        self.flask_app.config["GEODB_DIR"] = self.geodb_dir

    def tearDown(self):
        shutil.rmtree(self.flask_app.config["GEODB_DIR"])

    def testRootDir(self):
        with self.flask_app.app_context():
            storage_instance = storage.GeoDBRasterStorage()
            self.assertEquals(storage_instance.get_root_dir(), f"{self.geodb_dir}")

    def testTmpDir(self):
        with self.flask_app.app_context():
            storage_instance = storage.GeoDBRasterStorage()
            self.assertEquals(
                storage_instance.get_tmp_dir(), f"{self.geodb_cache_dir}/tmp"  # nosec
            )

    def testDir(self):
        with self.flask_app.app_context():
            storage_instance = storage.GeoDBRasterStorage()
            self.assertEquals(
                storage_instance.get_dir("raster/10"), f"{self.geodb_dir}/10"
            )
            self.assertEquals(
                storage_instance.get_dir("raster/10/2015"), f"{self.geodb_dir}/10"
            )
            self.assertEquals(
                storage_instance.get_dir(f"raster/10/2015/{ENCODED_VAR}"),
                f"{self.geodb_dir}/10",
            )
            self.assertEquals(
                storage_instance.get_dir(f"raster/10//{ENCODED_VAR}"),
                f"{self.geodb_dir}/10",
            )

    def testFilePath(self):
        with self.flask_app.app_context():
            storage_instance = storage.GeoDBRasterStorage()
            self.assertEquals(
                storage_instance.get_file_path("raster/10", "layer.tif"),
                f"{self.geodb_dir}/10/layer.tif",
            )
            self.assertEquals(
                storage_instance.get_file_path("raster/10/2015", "layer.tif"),
                f"{self.geodb_dir}/10/layer.tif",
            )
            self.assertEquals(
                storage_instance.get_file_path(
                    f"raster/10/2015/{ENCODED_VAR}", "layer.tif"
                ),
                f"{self.geodb_dir}/10/layer.tif",
            )
            self.assertEquals(
                storage_instance.get_file_path(
                    f"raster/10//{ENCODED_VAR}", "layer.tif"
                ),
                f"{self.geodb_dir}/10/layer.tif",
            )


class TestCMOutputStorage(BaseApiTest):
    def testRootDir(self):
        with self.flask_app.app_context():
            storage_instance = storage.CMOutputStorage()
            self.assertEquals(storage_instance.get_root_dir(), f"{self.cm_outputs_dir}")

    def testTmpDir(self):
        with self.flask_app.app_context():
            storage_instance = storage.CMOutputStorage()
            self.assertEquals(
                storage_instance.get_tmp_dir(), f"{self.cm_outputs_dir}/tmp"  # nosec
            )

    def testDir(self):
        with self.flask_app.app_context():
            storage_instance = storage.CMOutputStorage()
            self.assertEquals(
                storage_instance.get_dir("cm/some_name_12345678-000000"),
                f"{self.cm_outputs_dir}/some/name/12/34/56/some_name_12345678-000000",
            )

    def testFilePath(self):
        with self.flask_app.app_context():
            storage_instance = storage.CMOutputStorage()
            self.assertEquals(
                storage_instance.get_file_path(
                    "cm/some_name_12345678-000000", "result.tif"
                ),
                f"{self.cm_outputs_dir}/some/name/12/34/56/some_name_12345678-000000/result.tif",
            )


class TestGeoDBVectorStorage(BaseApiTest):
    def testRootDir(self):
        with self.flask_app.app_context():
            storage_instance = storage.GeoDBVectorStorage()
            self.assertEquals(
                storage_instance.get_root_dir(), f"{self.geodb_cache_dir}/vectors"
            )

    def testTmpDir(self):
        with self.flask_app.app_context():
            storage_instance = storage.GeoDBVectorStorage()
            self.assertEquals(
                storage_instance.get_tmp_dir(), f"{self.geodb_cache_dir}/tmp"  # nosec
            )

    def testDir(self):
        with self.flask_app.app_context():
            storage_instance = storage.GeoDBVectorStorage()
            self.assertEquals(
                storage_instance.get_dir("vector/10"),
                f"{self.geodb_cache_dir}/vectors/10",
            )
            self.assertEquals(
                storage_instance.get_dir("vector/10/2015"),
                f"{self.geodb_cache_dir}/vectors/10/2015",
            )
            self.assertEquals(
                storage_instance.get_dir(f"vector/10/2015/{ENCODED_VAR}"),
                f"{self.geodb_cache_dir}/vectors/10/2015/{ENCODED_VAR}",
            )
            self.assertEquals(
                storage_instance.get_dir(f"vector/10//{ENCODED_VAR}"),
                f"{self.geodb_cache_dir}/vectors/10/{ENCODED_VAR}",
            )

    def testShapefile(self):
        with self.flask_app.app_context():
            storage_instance = storage.GeoDBVectorStorage()
            self.assertEquals(
                storage_instance.get_shape_file("vector/10"),
                f"{self.geodb_cache_dir}/vectors/10/data.shp",
            )
            self.assertEquals(
                storage_instance.get_shape_file("vector/10/2015"),
                f"{self.geodb_cache_dir}/vectors/10/2015/data.shp",
            )
            self.assertEquals(
                storage_instance.get_shape_file(f"vector/10/2015/{ENCODED_VAR}"),
                f"{self.geodb_cache_dir}/vectors/10/2015/{ENCODED_VAR}/data.shp",
            )
            self.assertEquals(
                storage_instance.get_shape_file(f"vector/10//{ENCODED_VAR}"),
                f"{self.geodb_cache_dir}/vectors/10/{ENCODED_VAR}/data.shp",
            )


class TestAreaStorage(BaseApiTest):
    def testRootDir(self):
        with self.flask_app.app_context():
            storage_instance = storage.AreaStorage()
            self.assertEquals(
                storage_instance.get_root_dir(), f"{self.geodb_cache_dir}/areas"
            )

    def testTmpDir(self):
        with self.flask_app.app_context():
            storage_instance = storage.AreaStorage()
            self.assertEquals(
                storage_instance.get_tmp_dir(), f"{self.geodb_cache_dir}/tmp"  # nosec
            )

    def testDir(self):
        with self.flask_app.app_context():
            storage_instance = storage.AreaStorage()
            self.assertEquals(
                storage_instance.get_dir("area/NUTS42"),
                f"{self.geodb_cache_dir}/areas/NUTS42",
            )

    def testShapefile(self):
        with self.flask_app.app_context():
            storage_instance = storage.AreaStorage()
            self.assertEquals(
                storage_instance.get_shape_file("area/NUTS42"),
                f"{self.geodb_cache_dir}/areas/NUTS42/data.shp",
            )
