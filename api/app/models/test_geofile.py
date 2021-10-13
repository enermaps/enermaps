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
