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
