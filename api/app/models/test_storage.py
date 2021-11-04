import io
import json
import os
import shutil
import tempfile
import zipfile
from pathlib import Path

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
            self.assertTrue(isinstance(storage_instance, storage.RasterStorage))

    def testVector(self):
        with self.flask_app.app_context():
            storage_instance = storage.create("vector/42")
            self.assertTrue(storage_instance is not None)
            self.assertTrue(isinstance(storage_instance, storage.VectorStorage))

    def testCMOutput(self):
        with self.flask_app.app_context():
            storage_instance = storage.create("cm/blah")
            self.assertTrue(storage_instance is not None)
            self.assertTrue(isinstance(storage_instance, storage.CMStorage))

    def testUnknown(self):
        with self.flask_app.app_context():
            storage_instance = storage.create("unknown/blah")
            self.assertTrue(storage_instance is None)


class TestRasterStorage(BaseApiTest):
    def testRootDir(self):
        with self.flask_app.app_context():
            storage_instance = storage.RasterStorage()
            self.assertEquals(
                storage_instance.get_root_dir(), f"{self.wms_cache_dir}/rasters"
            )

    def testCacheRootDir(self):
        with self.flask_app.app_context():
            storage_instance = storage.RasterStorage()
            self.assertEquals(
                storage_instance.get_root_dir(cache=True),
                f"{self.wms_cache_dir}/rasters",
            )

    def testTmpDir(self):
        with self.flask_app.app_context():
            storage_instance = storage.RasterStorage()
            self.assertEquals(
                storage_instance.get_tmp_dir(), f"{self.wms_cache_dir}/tmp"  # nosec
            )

    def testDir(self):
        with self.flask_app.app_context():
            storage_instance = storage.RasterStorage()
            self.assertEquals(
                storage_instance.get_dir("raster/10"),
                f"{self.wms_cache_dir}/rasters/10",
            )
            self.assertEquals(
                storage_instance.get_dir("raster/10/2015"),
                f"{self.wms_cache_dir}/rasters/10/2015",
            )
            self.assertEquals(
                storage_instance.get_dir("raster/10/2015-01"),
                f"{self.wms_cache_dir}/rasters/10/2015-01",
            )
            self.assertEquals(
                storage_instance.get_dir("raster/10/None"),
                f"{self.wms_cache_dir}/rasters/10/None",
            )
            self.assertEquals(
                storage_instance.get_dir(f"raster/10/2015/{ENCODED_VAR}"),
                f"{self.wms_cache_dir}/rasters/10/2015/{ENCODED_VAR}",
            )
            self.assertEquals(
                storage_instance.get_dir(f"raster/10/2015-01/{ENCODED_VAR}"),
                f"{self.wms_cache_dir}/rasters/10/2015-01/{ENCODED_VAR}",
            )
            self.assertEquals(
                storage_instance.get_dir(f"raster/10/None/{ENCODED_VAR}"),
                f"{self.wms_cache_dir}/rasters/10/None/{ENCODED_VAR}",
            )
            self.assertEquals(
                storage_instance.get_dir(f"raster/10/-/{ENCODED_VAR}"),
                f"{self.wms_cache_dir}/rasters/10/{ENCODED_VAR}",
            )

    def testCacheDir(self):
        with self.flask_app.app_context():
            storage_instance = storage.RasterStorage()
            self.assertEquals(
                storage_instance.get_dir("raster/10", cache=True),
                f"{self.wms_cache_dir}/rasters/10",
            )
            self.assertEquals(
                storage_instance.get_dir("raster/10/2015", cache=True),
                f"{self.wms_cache_dir}/rasters/10/2015",
            )
            self.assertEquals(
                storage_instance.get_dir("raster/10/2015-01", cache=True),
                f"{self.wms_cache_dir}/rasters/10/2015-01",
            )
            self.assertEquals(
                storage_instance.get_dir("raster/10/None", cache=True),
                f"{self.wms_cache_dir}/rasters/10/None",
            )
            self.assertEquals(
                storage_instance.get_dir(f"raster/10/2015/{ENCODED_VAR}", cache=True),
                f"{self.wms_cache_dir}/rasters/10/2015/{ENCODED_VAR}",
            )
            self.assertEquals(
                storage_instance.get_dir(
                    f"raster/10/2015-01/{ENCODED_VAR}", cache=True
                ),
                f"{self.wms_cache_dir}/rasters/10/2015-01/{ENCODED_VAR}",
            )
            self.assertEquals(
                storage_instance.get_dir(f"raster/10/None/{ENCODED_VAR}", cache=True),
                f"{self.wms_cache_dir}/rasters/10/None/{ENCODED_VAR}",
            )
            self.assertEquals(
                storage_instance.get_dir(f"raster/10/-/{ENCODED_VAR}", cache=True),
                f"{self.wms_cache_dir}/rasters/10/{ENCODED_VAR}",
            )

    def testFilePath(self):
        with self.flask_app.app_context():
            storage_instance = storage.RasterStorage()
            self.assertEquals(
                storage_instance.get_file_path("raster/10", "layer.tif"),
                f"{self.wms_cache_dir}/rasters/10/layer.tif",
            )
            self.assertEquals(
                storage_instance.get_file_path("raster/10/2015", "layer.tif"),
                f"{self.wms_cache_dir}/rasters/10/2015/layer.tif",
            )
            self.assertEquals(
                storage_instance.get_file_path("raster/10/2015-01", "layer.tif"),
                f"{self.wms_cache_dir}/rasters/10/2015-01/layer.tif",
            )
            self.assertEquals(
                storage_instance.get_file_path("raster/10/None", "layer.tif"),
                f"{self.wms_cache_dir}/rasters/10/None/layer.tif",
            )
            self.assertEquals(
                storage_instance.get_file_path(
                    f"raster/10/2015/{ENCODED_VAR}", "layer.tif"
                ),
                f"{self.wms_cache_dir}/rasters/10/2015/{ENCODED_VAR}/layer.tif",
            )
            self.assertEquals(
                storage_instance.get_file_path(
                    f"raster/10/2015-01/{ENCODED_VAR}", "layer.tif"
                ),
                f"{self.wms_cache_dir}/rasters/10/2015-01/{ENCODED_VAR}/layer.tif",
            )
            self.assertEquals(
                storage_instance.get_file_path(
                    f"raster/10/None/{ENCODED_VAR}", "layer.tif"
                ),
                f"{self.wms_cache_dir}/rasters/10/None/{ENCODED_VAR}/layer.tif",
            )
            self.assertEquals(
                storage_instance.get_file_path(
                    f"raster/10/-/{ENCODED_VAR}", "layer.tif"
                ),
                f"{self.wms_cache_dir}/rasters/10/{ENCODED_VAR}/layer.tif",
            )

    def testListFeatureIds(self):
        with self.flask_app.app_context():
            storage_instance = storage.RasterStorage()

            layer_name = "raster/10"

            folder = storage_instance.get_dir(layer_name)

            os.makedirs(folder)
            Path(os.path.join(folder, "FID1.tif")).touch()
            Path(os.path.join(folder, "FID2.tif")).touch()

            features = storage_instance.list_feature_ids(layer_name)

            self.assertTrue(isinstance(features, list))
            self.assertEqual(len(features), 2)
            self.assertTrue("FID1.tif" in features)
            self.assertTrue("FID2.tif" in features)

    def testListFeatureIdsWithSubfolders(self):
        with self.flask_app.app_context():
            storage_instance = storage.RasterStorage()

            layer_name = "raster/10"

            folder = storage_instance.get_dir(layer_name)

            os.makedirs(os.path.join(folder, "subfolder1"))
            Path(os.path.join(folder, "subfolder1/FID1.tif")).touch()
            Path(os.path.join(folder, "subfolder1/FID2.tif")).touch()

            os.makedirs(os.path.join(folder, "subfolder2"))
            Path(os.path.join(folder, "subfolder2/FID3.tif")).touch()
            Path(os.path.join(folder, "subfolder2/FID4.tif")).touch()

            features = storage_instance.list_feature_ids(layer_name)

            self.assertTrue(isinstance(features, list))
            self.assertEqual(len(features), 4)
            self.assertTrue("subfolder1/FID1.tif" in features)
            self.assertTrue("subfolder1/FID2.tif" in features)
            self.assertTrue("subfolder2/FID3.tif" in features)
            self.assertTrue("subfolder2/FID4.tif" in features)

    def testGetGeometries(self):
        with self.flask_app.app_context():
            storage_instance = storage.RasterStorage()

            layer_name = "raster/10"

            GEOMETRIES = {
                "FID1.tif": [
                    [2.29753807249901, 48.8755536106299],
                    [2.29614325745428, 48.8844921519625],
                    [2.28257324809059, 48.8835519677318],
                    [2.28397047391374, 48.8746136217482],
                    [2.29753807249901, 48.8755536106299],
                ]
            }

            os.makedirs(storage_instance.get_dir(layer_name))

            filename = os.path.join(
                storage_instance.get_dir(layer_name), "geometries.json"
            )
            with open(filename, "w") as f:
                json.dump(GEOMETRIES, f)

            geometries = storage_instance.get_geometries(layer_name)

            self.assertEqual(geometries, GEOMETRIES)

    def testGetBBox(self):
        with self.flask_app.app_context():
            storage_instance = storage.RasterStorage()

            layer_name = "raster/10"

            BBOX = {
                "left": 10,
                "right": 20,
                "bottom": 30,
                "top": 40,
            }

            os.makedirs(storage_instance.get_dir(layer_name))

            filename = os.path.join(storage_instance.get_dir(layer_name), "bbox.json")
            with open(filename, "w") as f:
                json.dump(BBOX, f)

            bbox = storage_instance.get_bbox(layer_name)

            self.assertEqual(bbox, BBOX)

    def testGetBBoxMissingFile(self):
        with self.flask_app.app_context():
            storage_instance = storage.RasterStorage()

            layer_name = "raster/10"

            bbox = storage_instance.get_bbox(layer_name)
            self.assertTrue(bbox is None)


class TestRasterStorageWithoutCache(BaseApiTest):
    def setUp(self):
        super().setUp()
        self.raster_cache_dir = tempfile.mkdtemp()
        self.flask_app.config["RASTER_CACHE_DIR"] = self.raster_cache_dir

    def tearDown(self):
        shutil.rmtree(self.flask_app.config["RASTER_CACHE_DIR"])

    def testRootDir(self):
        with self.flask_app.app_context():
            storage_instance = storage.RasterStorage()
            self.assertEquals(
                storage_instance.get_root_dir(), f"{self.raster_cache_dir}"
            )

    def testTmpDir(self):
        with self.flask_app.app_context():
            storage_instance = storage.RasterStorage()
            self.assertEquals(
                storage_instance.get_tmp_dir(), f"{self.wms_cache_dir}/tmp"  # nosec
            )

    def testDir(self):
        with self.flask_app.app_context():
            storage_instance = storage.RasterStorage()
            self.assertEquals(
                storage_instance.get_dir("raster/10"), f"{self.raster_cache_dir}/10"
            )
            self.assertEquals(
                storage_instance.get_dir("raster/10/2015"),
                f"{self.raster_cache_dir}/10",
            )
            self.assertEquals(
                storage_instance.get_dir("raster/10/2015-01"),
                f"{self.raster_cache_dir}/10",
            )
            self.assertEquals(
                storage_instance.get_dir("raster/10/None"),
                f"{self.raster_cache_dir}/10",
            )
            self.assertEquals(
                storage_instance.get_dir(f"raster/10/2015/{ENCODED_VAR}"),
                f"{self.raster_cache_dir}/10",
            )
            self.assertEquals(
                storage_instance.get_dir(f"raster/10/2015-01/{ENCODED_VAR}"),
                f"{self.raster_cache_dir}/10",
            )
            self.assertEquals(
                storage_instance.get_dir(f"raster/10/None/{ENCODED_VAR}"),
                f"{self.raster_cache_dir}/10",
            )
            self.assertEquals(
                storage_instance.get_dir(f"raster/10/-/{ENCODED_VAR}"),
                f"{self.raster_cache_dir}/10",
            )

    def testFilePath(self):
        with self.flask_app.app_context():
            storage_instance = storage.RasterStorage()
            self.assertEquals(
                storage_instance.get_file_path("raster/10", "layer.tif"),
                f"{self.raster_cache_dir}/10/layer.tif",
            )
            self.assertEquals(
                storage_instance.get_file_path("raster/10/2015", "layer.tif"),
                f"{self.raster_cache_dir}/10/layer.tif",
            )
            self.assertEquals(
                storage_instance.get_file_path("raster/10/2015-01", "layer.tif"),
                f"{self.raster_cache_dir}/10/layer.tif",
            )
            self.assertEquals(
                storage_instance.get_file_path("raster/10/None", "layer.tif"),
                f"{self.raster_cache_dir}/10/layer.tif",
            )
            self.assertEquals(
                storage_instance.get_file_path(
                    f"raster/10/2015/{ENCODED_VAR}", "layer.tif"
                ),
                f"{self.raster_cache_dir}/10/layer.tif",
            )
            self.assertEquals(
                storage_instance.get_file_path(
                    f"raster/10/2015-01/{ENCODED_VAR}", "layer.tif"
                ),
                f"{self.raster_cache_dir}/10/layer.tif",
            )
            self.assertEquals(
                storage_instance.get_file_path(
                    f"raster/10/None/{ENCODED_VAR}", "layer.tif"
                ),
                f"{self.raster_cache_dir}/10/layer.tif",
            )
            self.assertEquals(
                storage_instance.get_file_path(
                    f"raster/10/-/{ENCODED_VAR}", "layer.tif"
                ),
                f"{self.raster_cache_dir}/10/layer.tif",
            )

    def testGetGeometries(self):
        with self.flask_app.app_context():
            storage_instance = storage.RasterStorage()

            layer_name = "raster/10"

            GEOMETRIES = {
                "FID1.tif": [
                    [2.29753807249901, 48.8755536106299],
                    [2.29614325745428, 48.8844921519625],
                    [2.28257324809059, 48.8835519677318],
                    [2.28397047391374, 48.8746136217482],
                    [2.29753807249901, 48.8755536106299],
                ]
            }

            os.makedirs(storage_instance.get_dir(layer_name, cache=True))

            filename = os.path.join(
                storage_instance.get_dir(layer_name, cache=True), "geometries.json"
            )
            with open(filename, "w") as f:
                json.dump(GEOMETRIES, f)

            geometries = storage_instance.get_geometries(layer_name)

            self.assertEqual(geometries, GEOMETRIES)

    def testGetBBox(self):
        with self.flask_app.app_context():
            storage_instance = storage.RasterStorage()

            layer_name = "raster/10"

            BBOX = {
                "left": 10,
                "right": 20,
                "bottom": 30,
                "top": 40,
            }

            os.makedirs(storage_instance.get_dir(layer_name, cache=True))

            filename = os.path.join(
                storage_instance.get_dir(layer_name, cache=True), "bbox.json"
            )
            with open(filename, "w") as f:
                json.dump(BBOX, f)

            bbox = storage_instance.get_bbox(layer_name)

            self.assertEqual(bbox, BBOX)

    def testGetBBoxMissingFile(self):
        with self.flask_app.app_context():
            storage_instance = storage.RasterStorage()

            layer_name = "raster/10"

            bbox = storage_instance.get_bbox(layer_name)
            self.assertTrue(bbox is None)


class TestCMStorage(BaseApiTest):
    def testRootDir(self):
        with self.flask_app.app_context():
            storage_instance = storage.CMStorage()
            self.assertEquals(storage_instance.get_root_dir(), f"{self.cm_outputs_dir}")

    def testTmpDir(self):
        with self.flask_app.app_context():
            storage_instance = storage.CMStorage()
            self.assertEquals(
                storage_instance.get_tmp_dir(), f"{self.cm_outputs_dir}/tmp"  # nosec
            )

    def testDir(self):
        with self.flask_app.app_context():
            storage_instance = storage.CMStorage()
            self.assertEquals(
                storage_instance.get_dir(
                    "cm/some_name/01234567-0000-0000-0000-000000000000"
                ),
                f"{self.cm_outputs_dir}/some_name/01/23/45/67/01234567-0000-0000-0000-000000000000",
            )

    def testFilePath(self):
        with self.flask_app.app_context():
            storage_instance = storage.CMStorage()
            self.assertEquals(
                storage_instance.get_file_path(
                    "cm/some_name/01234567-0000-0000-0000-000000000000", "result.tif"
                ),
                f"{self.cm_outputs_dir}/some_name/01/23/45/67/01234567-0000-0000-0000-000000000000/result.tif",
            )

    def testAsZip(self):
        with self.flask_app.app_context():
            storage_instance = storage.CMStorage()
            layer_name = "cm/some_name/01234567-0000-0000-0000-000000000000"

            os.makedirs(storage_instance.get_dir(layer_name))

            with open(storage_instance.get_file_path(layer_name, "data.prj"), "w") as f:
                f.write("PROJECTION")

            with open(
                storage_instance.get_file_path(layer_name, "parameters.json"), "w"
            ) as f:
                f.write("PARAMETERS")

            with open(
                storage_instance.get_file_path(layer_name, "result.json"), "w"
            ) as f:
                f.write("RESULT")

            raster_filename = self.get_testdata_path("hotmaps-cdd_curr_adapted.tif")

            shutil.copy(
                raster_filename, storage_instance.get_file_path(layer_name, "data.tif")
            )

            content = storage_instance.as_zip(layer_name)

            self.assertTrue(content is not None)
            self.assertTrue(isinstance(content, io.BytesIO))

            with zipfile.ZipFile(content, "r") as zip_file:
                filenames = zip_file.namelist()
                self.assertEqual(len(filenames), 4)
                self.assertTrue("data.prj" in filenames)
                self.assertTrue("parameters.json" in filenames)
                self.assertTrue("result.json" in filenames)
                self.assertTrue("data.tif" in filenames)

                with zip_file.open("data.prj", "r") as f:
                    self.assertEqual(f.read(), b"PROJECTION")

                with zip_file.open("parameters.json", "r") as f:
                    self.assertEqual(f.read(), b"PARAMETERS")

                with zip_file.open("result.json", "r") as f:
                    self.assertEqual(f.read(), b"RESULT")

                with zip_file.open("data.tif", "r") as f:
                    with open(raster_filename, "rb") as f2:
                        self.assertEqual(f.read(), f2.read())

    def testAsZipWithNotExistingDirectory(self):
        with self.flask_app.app_context():
            storage_instance = storage.CMStorage()
            layer_name = "cm/some_name/01234567-0000-0000-0000-000000000000"

            os.makedirs(storage_instance.get_dir(layer_name))

            content = storage_instance.as_zip(layer_name)

            self.assertTrue(content is None)

    def testAsZipWithEmptyDirectory(self):
        with self.flask_app.app_context():
            storage_instance = storage.CMStorage()
            layer_name = "cm/some_name/01234567-0000-0000-0000-000000000000"

            content = storage_instance.as_zip(layer_name)

            self.assertTrue(content is None)


class TestVectorStorage(BaseApiTest):
    def testRootDir(self):
        with self.flask_app.app_context():
            storage_instance = storage.VectorStorage()
            self.assertEquals(
                storage_instance.get_root_dir(), f"{self.wms_cache_dir}/vectors"
            )

    def testTmpDir(self):
        with self.flask_app.app_context():
            storage_instance = storage.VectorStorage()
            self.assertEquals(
                storage_instance.get_tmp_dir(), f"{self.wms_cache_dir}/tmp"  # nosec
            )

    def testDir(self):
        with self.flask_app.app_context():
            storage_instance = storage.VectorStorage()
            self.assertEquals(
                storage_instance.get_dir("vector/10"),
                f"{self.wms_cache_dir}/vectors/10",
            )
            self.assertEquals(
                storage_instance.get_dir("vector/10/2015"),
                f"{self.wms_cache_dir}/vectors/10/2015",
            )
            self.assertEquals(
                storage_instance.get_dir("vector/10/2015-01"),
                f"{self.wms_cache_dir}/vectors/10/2015-01",
            )
            self.assertEquals(
                storage_instance.get_dir("vector/10/None"),
                f"{self.wms_cache_dir}/vectors/10/None",
            )
            self.assertEquals(
                storage_instance.get_dir(f"vector/10/2015/{ENCODED_VAR}"),
                f"{self.wms_cache_dir}/vectors/10/2015",
            )
            self.assertEquals(
                storage_instance.get_dir(f"vector/10/2015-01/{ENCODED_VAR}"),
                f"{self.wms_cache_dir}/vectors/10/2015-01",
            )
            self.assertEquals(
                storage_instance.get_dir(f"vector/10/None/{ENCODED_VAR}"),
                f"{self.wms_cache_dir}/vectors/10/None",
            )
            self.assertEquals(
                storage_instance.get_dir(f"vector/10/-/{ENCODED_VAR}"),
                f"{self.wms_cache_dir}/vectors/10",
            )

    def testFilePath(self):
        with self.flask_app.app_context():
            storage_instance = storage.VectorStorage()
            self.assertEquals(
                storage_instance.get_file_path("vector/10", "data.txt"),
                f"{self.wms_cache_dir}/vectors/10/data.txt",
            )
            self.assertEquals(
                storage_instance.get_file_path("vector/10/2015", "data.txt"),
                f"{self.wms_cache_dir}/vectors/10/2015/data.txt",
            )
            self.assertEquals(
                storage_instance.get_file_path("vector/10/2015-01", "data.txt"),
                f"{self.wms_cache_dir}/vectors/10/2015-01/data.txt",
            )
            self.assertEquals(
                storage_instance.get_file_path("vector/10/None", "data.txt"),
                f"{self.wms_cache_dir}/vectors/10/None/data.txt",
            )
            self.assertEquals(
                storage_instance.get_file_path(
                    f"vector/10/2015/{ENCODED_VAR}", "data.txt"
                ),
                f"{self.wms_cache_dir}/vectors/10/2015/data.txt",
            )
            self.assertEquals(
                storage_instance.get_file_path(
                    f"vector/10/2015-01/{ENCODED_VAR}", "data.txt"
                ),
                f"{self.wms_cache_dir}/vectors/10/2015-01/data.txt",
            )
            self.assertEquals(
                storage_instance.get_file_path(
                    f"vector/10/None/{ENCODED_VAR}", "data.txt"
                ),
                f"{self.wms_cache_dir}/vectors/10/None/data.txt",
            )
            self.assertEquals(
                storage_instance.get_file_path(
                    f"vector/10/-/{ENCODED_VAR}", "data.txt"
                ),
                f"{self.wms_cache_dir}/vectors/10/data.txt",
            )

    def testGeoJSONFile(self):
        with self.flask_app.app_context():
            storage_instance = storage.VectorStorage()
            self.assertEquals(
                storage_instance.get_geojson_file("vector/10"),
                f"{self.wms_cache_dir}/vectors/10/data.geojson",
            )
            self.assertEquals(
                storage_instance.get_geojson_file("vector/10/2015"),
                f"{self.wms_cache_dir}/vectors/10/2015/data.geojson",
            )
            self.assertEquals(
                storage_instance.get_geojson_file("vector/10/2015-01"),
                f"{self.wms_cache_dir}/vectors/10/2015-01/data.geojson",
            )
            self.assertEquals(
                storage_instance.get_geojson_file("vector/10/None"),
                f"{self.wms_cache_dir}/vectors/10/None/data.geojson",
            )
            self.assertEquals(
                storage_instance.get_geojson_file(f"vector/10/2015/{ENCODED_VAR}"),
                f"{self.wms_cache_dir}/vectors/10/2015/data.geojson",
            )
            self.assertEquals(
                storage_instance.get_geojson_file(f"vector/10/2015-01/{ENCODED_VAR}"),
                f"{self.wms_cache_dir}/vectors/10/2015-01/data.geojson",
            )
            self.assertEquals(
                storage_instance.get_geojson_file(f"vector/10/None/{ENCODED_VAR}"),
                f"{self.wms_cache_dir}/vectors/10/None/data.geojson",
            )
            self.assertEquals(
                storage_instance.get_geojson_file(f"vector/10/-/{ENCODED_VAR}"),
                f"{self.wms_cache_dir}/vectors/10/data.geojson",
            )

    def testGetBBox(self):
        with self.flask_app.app_context():
            storage_instance = storage.RasterStorage()

            layer_name = "vector/10"

            BBOX = {
                "left": 10,
                "right": 20,
                "bottom": 30,
                "top": 40,
            }

            os.makedirs(storage_instance.get_dir(layer_name))

            filename = os.path.join(storage_instance.get_dir(layer_name), "bbox.json")
            with open(filename, "w") as f:
                json.dump(BBOX, f)

            bbox = storage_instance.get_bbox(layer_name)

            self.assertEqual(bbox, BBOX)

    def testGetBBoxMissingFile(self):
        with self.flask_app.app_context():
            storage_instance = storage.RasterStorage()

            layer_name = "vector/10"

            bbox = storage_instance.get_bbox(layer_name)
            self.assertTrue(bbox is None)


class TestAreaStorage(BaseApiTest):
    def testRootDir(self):
        with self.flask_app.app_context():
            storage_instance = storage.AreaStorage()
            self.assertEquals(
                storage_instance.get_root_dir(), f"{self.wms_cache_dir}/areas"
            )

    def testTmpDir(self):
        with self.flask_app.app_context():
            storage_instance = storage.AreaStorage()
            self.assertEquals(
                storage_instance.get_tmp_dir(), f"{self.wms_cache_dir}/tmp"  # nosec
            )

    def testDir(self):
        with self.flask_app.app_context():
            storage_instance = storage.AreaStorage()
            self.assertEquals(
                storage_instance.get_dir("area/NUTS42"),
                f"{self.wms_cache_dir}/areas/NUTS42",
            )

    def testGeoJSONFile(self):
        with self.flask_app.app_context():
            storage_instance = storage.AreaStorage()
            self.assertEquals(
                storage_instance.get_geojson_file("area/NUTS42"),
                f"{self.wms_cache_dir}/areas/NUTS42/data.geojson",
            )
