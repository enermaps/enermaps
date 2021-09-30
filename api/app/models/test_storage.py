import shutil
import tempfile

from app.common.test import BaseApiTest
from app.models.storage import CMOutputStorage, GeoDBRasterStorage, GeoDBVectorStorage


class TestGeoDBRasterStorage(BaseApiTest):
    def testRootDir(self):
        with self.flask_app.app_context():
            storage = GeoDBRasterStorage()
            self.assertEquals(storage.get_root_dir(), f"{self.geodb_cache_dir}/rasters")

    def testTmpDir(self):
        with self.flask_app.app_context():
            storage = GeoDBRasterStorage()
            self.assertEquals(
                storage.get_tmp_dir(), f"{self.geodb_cache_dir}/tmp"  # nosec
            )

    def testDir(self):
        with self.flask_app.app_context():
            storage = GeoDBRasterStorage()
            self.assertEquals(storage.get_dir(10), f"{self.geodb_cache_dir}/rasters/10")

    def testFilePath(self):
        with self.flask_app.app_context():
            storage = GeoDBRasterStorage()
            self.assertEquals(
                storage.get_file_path(10, "layer.tif"),
                f"{self.geodb_cache_dir}/rasters/10/layer.tif",
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
            storage = GeoDBRasterStorage()
            self.assertEquals(storage.get_root_dir(), f"{self.geodb_dir}")

    def testTmpDir(self):
        with self.flask_app.app_context():
            storage = GeoDBRasterStorage()
            self.assertEquals(
                storage.get_tmp_dir(), f"{self.geodb_cache_dir}/tmp"  # nosec
            )

    def testDir(self):
        with self.flask_app.app_context():
            storage = GeoDBRasterStorage()
            self.assertEquals(storage.get_dir(10), f"{self.geodb_dir}/10")

    def testFilePath(self):
        with self.flask_app.app_context():
            storage = GeoDBRasterStorage()
            self.assertEquals(
                storage.get_file_path(10, "layer.tif"), f"{self.geodb_dir}/10/layer.tif"
            )


class TestCMOutputStorage(BaseApiTest):
    def testRootDir(self):
        with self.flask_app.app_context():
            storage = CMOutputStorage()
            self.assertEquals(storage.get_root_dir(), f"{self.cm_outputs_dir}")

    def testTmpDir(self):
        with self.flask_app.app_context():
            storage = CMOutputStorage()
            self.assertEquals(
                storage.get_tmp_dir(), f"{self.cm_outputs_dir}/tmp"  # nosec
            )

    def testDir(self):
        with self.flask_app.app_context():
            storage = CMOutputStorage()
            self.assertEquals(
                storage.get_dir("some_name_12345678-000000"),
                f"{self.cm_outputs_dir}/some/name/12/34/56/some_name_12345678-000000",
            )

    def testFilePath(self):
        with self.flask_app.app_context():
            storage = CMOutputStorage()
            self.assertEquals(
                storage.get_file_path("some_name_12345678-000000", "result.tif"),
                f"{self.cm_outputs_dir}/some/name/12/34/56/some_name_12345678-000000/result.tif",
            )


class TestGeoDBVectorStorage(BaseApiTest):
    def testRootDir(self):
        with self.flask_app.app_context():
            storage = GeoDBVectorStorage()
            self.assertEquals(storage.get_root_dir(), f"{self.geodb_cache_dir}/vectors")

    def testTmpDir(self):
        with self.flask_app.app_context():
            storage = GeoDBVectorStorage()
            self.assertEquals(
                storage.get_tmp_dir(), f"{self.geodb_cache_dir}/tmp"  # nosec
            )

    def testDir(self):
        with self.flask_app.app_context():
            storage = GeoDBVectorStorage()
            self.assertEquals(storage.get_dir(10), f"{self.geodb_cache_dir}/vectors/10")

    def testFilePath(self):
        with self.flask_app.app_context():
            storage = GeoDBVectorStorage()
            self.assertEquals(
                storage.get_file_path(10, "layer"),
                f"{self.geodb_cache_dir}/vectors/10/layer",
            )
