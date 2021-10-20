import json
import os

from app.common.test import BaseApiTest

from . import geofile, storage


class TestLoad(BaseApiTest):
    def testArea(self):
        with self.flask_app.app_context():
            layer = geofile.load("area/NUTS42")
            self.assertTrue(layer is not None)
            self.assertEqual(layer.name, "area/NUTS42")
            self.assertTrue(isinstance(layer.storage, storage.AreaStorage))

    def testRaster(self):
        with self.flask_app.app_context():
            layer = geofile.load("raster/42")
            self.assertTrue(layer is not None)
            self.assertEqual(layer.name, "raster/42")
            self.assertTrue(isinstance(layer.storage, storage.RasterStorage))

    def testVector(self):
        with self.flask_app.app_context():
            layer = geofile.load("vector/42")
            self.assertTrue(layer is not None)
            self.assertEqual(layer.name, "vector/42")
            self.assertTrue(isinstance(layer.storage, storage.VectorStorage))

    def testCMOutput(self):
        with self.flask_app.app_context():
            layer = geofile.load("cm/blah")
            self.assertTrue(layer is not None)
            self.assertEqual(layer.name, "cm/blah")
            self.assertTrue(isinstance(layer.storage, storage.CMStorage))


class TestSaveRasterFile(BaseApiTest):
    def testSimple(self):
        with self.flask_app.app_context():
            self.assertTrue(
                geofile.save_raster_file("raster/42", "file.txt", b"Hello world")
            )

            storage_instance = storage.create("raster/42")
            self.assertTrue(
                os.path.exists(storage_instance.get_file_path("raster/42", "file.txt"))
            )

    def testWithSubFolders(self):
        with self.flask_app.app_context():
            self.assertTrue(
                geofile.save_raster_file(
                    "raster/42", "subfolder/file.txt", b"Hello world"
                )
            )

            storage_instance = storage.create("raster/42")
            self.assertTrue(
                os.path.exists(
                    storage_instance.get_file_path("raster/42", "subfolder/file.txt")
                )
            )


class TestSaveCMFile(BaseApiTest):
    def testSave(self):
        with self.flask_app.app_context():
            layer_name = "cm/some_name/01234567-0000-0000-0000-000000000000"

            self.assertTrue(
                geofile.save_cm_file(layer_name, "file.txt", b"Hello world")
            )

            storage_instance = storage.create(layer_name)
            self.assertTrue(
                os.path.exists(storage_instance.get_file_path(layer_name, "file.txt"))
            )


class TestSaveCMResult(BaseApiTest):
    RESULT = {
        "legend": {
            "symbology": [],
        }
    }

    def testSaveResult(self):
        with self.flask_app.app_context():
            layer_name = "cm/some_name/01234567-0000-0000-0000-000000000000"

            self.assertTrue(geofile.save_cm_result(layer_name, TestSaveCMResult.RESULT))

            storage_instance = storage.create(layer_name)
            self.assertTrue(
                os.path.exists(
                    storage_instance.get_file_path(layer_name, "result.json")
                )
            )

            legend = geofile.get_cm_legend(layer_name)

            self.assertTrue(legend is not None)
            self.assertEqual(legend, TestSaveCMResult.RESULT["legend"])


class TestSaveCMParameters(BaseApiTest):
    PARAMETERS = {
        "selection": {},
        "layer": "raster/42/file.tif",
        "parameters": {},
    }

    def testSaveParameters(self):
        with self.flask_app.app_context():
            layer_name = "cm/some_name/01234567-0000-0000-0000-000000000000"

            self.assertTrue(
                geofile.save_cm_parameters(layer_name, TestSaveCMParameters.PARAMETERS)
            )

            storage_instance = storage.create(layer_name)
            filename = storage_instance.get_file_path(layer_name, "parameters.json")

            self.assertTrue(os.path.exists(filename))

            with open(filename, "r") as f:
                data = json.load(f)

            self.assertEqual(data, TestSaveCMParameters.PARAMETERS)
