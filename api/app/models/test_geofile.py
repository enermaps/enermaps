import copy
import json
import os

from app.common import path
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


class TestSaveVectorGeoJSON(BaseApiTest):
    GEOJSON = {
        "type": "FeatureCollection",
        "features": [
            {
                "id": "FEATURE_ID",
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [7.4, 46.0],
                },
                "properties": {
                    "units": {"var1": "MW", "var2": "kWh", "var3": "kWh"},
                    "fields": {
                        "field1": "value1",
                    },
                    "legend": {"symbology": []},
                    "start_at": None,
                    "variables": {
                        "var1": 1000,
                        "var2": 2000,
                        "var3": None,
                    },
                },
            }
        ],
    }

    def testFilesCreation(self):
        with self.flask_app.app_context():
            layer_name = "vector/42"

            valid_variables = geofile.save_vector_geojson(
                layer_name, copy.deepcopy(TestSaveVectorGeoJSON.GEOJSON)
            )
            self.assertTrue(valid_variables is not None)
            self.assertTrue(isinstance(valid_variables, list))
            self.assertTrue("var1" in valid_variables)
            self.assertTrue("var2" in valid_variables)
            self.assertTrue("var3" not in valid_variables)

            self.assertTrue(
                os.path.exists(f"{self.wms_cache_dir}/vectors/42/data.geojson")
            )
            self.assertTrue(os.path.exists(f"{self.wms_cache_dir}/vectors/42/data.prj"))
            self.assertTrue(
                os.path.exists(f"{self.wms_cache_dir}/vectors/42/variables.json")
            )

    def testGeoJSONFile(self):
        with self.flask_app.app_context():
            layer_name = "vector/42"

            geofile.save_vector_geojson(
                layer_name, copy.deepcopy(TestSaveVectorGeoJSON.GEOJSON)
            )

            with open(f"{self.wms_cache_dir}/vectors/42/data.geojson", "r") as f:
                geojson = json.load(f)

            self.assertEqual(len(geojson["features"]), 1)
            self.assertTrue("legend" not in geojson["features"][0]["properties"])
            self.assertTrue("__variable__var1" in geojson["features"][0]["properties"])
            self.assertTrue("__variable__var2" in geojson["features"][0]["properties"])
            self.assertTrue("__variable__var3" in geojson["features"][0]["properties"])

    def testVariablesFile(self):
        with self.flask_app.app_context():
            layer_name = "vector/42"

            geofile.save_vector_geojson(
                layer_name, copy.deepcopy(TestSaveVectorGeoJSON.GEOJSON)
            )

            with open(f"{self.wms_cache_dir}/vectors/42/variables.json", "r") as f:
                variables = json.load(f)

            self.assertTrue(isinstance(variables, list))
            self.assertTrue("var1" in variables)
            self.assertTrue("var2" in variables)
            self.assertTrue("var3" not in variables)


class TestSaveRasterProjection(BaseApiTest):
    def testFileCreation(self):
        with self.flask_app.app_context():
            layer_name = "raster/42"

            geofile.save_raster_projection(layer_name, "EPSG:3857")

            self.assertTrue(
                os.path.exists(f"{self.wms_cache_dir}/rasters/42/projection.txt")
            )

    def testFileCreationWithFullLayerName(self):
        with self.flask_app.app_context():
            layer_name = path.make_unique_layer_name(
                path.RASTER, 42, time_period="2015", variable="variable"
            )

            geofile.save_raster_projection(layer_name, "EPSG:3857")

            self.assertTrue(
                os.path.exists(f"{self.wms_cache_dir}/rasters/42/projection.txt")
            )

    def testFileContent(self):
        with self.flask_app.app_context():
            layer_name = "raster/42"

            geofile.save_raster_projection(layer_name, "EPSG:3857")

            with open(f"{self.wms_cache_dir}/rasters/42/projection.txt", "r") as f:
                data = f.read()

            self.assertEqual(data, "EPSG:3857")


class TestSaveRasterGeometries(BaseApiTest):
    GEOJSON = {
        "type": "FeatureCollection",
        "features": [
            {
                "id": "FID1.tif",
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [10, 30],
                            [20, 30],
                            [20, 40],
                            [10, 40],
                            [10, 30],
                        ],
                    ],
                },
                "properties": {
                    "units": {"var1": "MW", "var2": "kWh", "var3": "kWh"},
                    "fields": {
                        "field1": "value1",
                    },
                    "legend": {"symbology": []},
                    "start_at": None,
                    "variables": {
                        "var1": None,
                        "var2": None,
                        "var3": None,
                    },
                },
            }
        ],
    }

    def testSuccess(self):
        with self.flask_app.app_context():
            layer_name = path.make_unique_layer_name(
                path.RASTER, 42, time_period="2015", variable="variable"
            )

            geofile.save_raster_geometries(
                layer_name, copy.deepcopy(TestSaveRasterGeometries.GEOJSON)
            )

            folder = path.to_folder_path(layer_name)
            filename = f"{self.wms_cache_dir}/rasters/{folder}/geometries.json"

            self.assertTrue(os.path.exists(filename))

            with open(filename, "r") as f:
                geometries = json.load(f)

            self.assertEqual(len(geometries), 1)
            self.assertTrue("FID1.tif" in geometries)

            polygon = geometries["FID1.tif"]
            self.assertTrue(isinstance(polygon, list))
            self.assertEqual(len(polygon), 5)

            for i in range(len(polygon)):
                self.assertEqual(
                    polygon[i],
                    TestSaveRasterGeometries.GEOJSON["features"][0]["geometry"][
                        "coordinates"
                    ][0][i],
                )

    def testFailureNoFeatures(self):
        with self.flask_app.app_context():
            layer_name = path.make_unique_layer_name(
                path.RASTER, 42, time_period="2015", variable="variable"
            )

            geojson = copy.deepcopy(TestSaveRasterGeometries.GEOJSON)
            geojson["features"] = []

            geofile.save_raster_geometries(layer_name, geojson)

            folder = path.to_folder_path(layer_name)
            self.assertFalse(
                os.path.exists(f"{self.wms_cache_dir}/rasters/{folder}/geometries.json")
            )

    def testFailureNoGeometry(self):
        with self.flask_app.app_context():
            layer_name = path.make_unique_layer_name(
                path.RASTER, 42, time_period="2015", variable="variable"
            )

            geojson = copy.deepcopy(TestSaveRasterGeometries.GEOJSON)
            geojson["features"][0]["geometry"] = None

            geofile.save_raster_geometries(layer_name, geojson)

            folder = path.to_folder_path(layer_name)
            self.assertFalse(
                os.path.exists(f"{self.wms_cache_dir}/rasters/{folder}/geometries.json")
            )

    def testFailureNotPolygon(self):
        with self.flask_app.app_context():
            layer_name = path.make_unique_layer_name(
                path.RASTER, 42, time_period="2015", variable="variable"
            )

            geojson = copy.deepcopy(TestSaveRasterGeometries.GEOJSON)
            geojson["features"][0]["geometry"]["type"] = "Point"

            geofile.save_raster_geometries(layer_name, geojson)

            folder = path.to_folder_path(layer_name)
            self.assertFalse(
                os.path.exists(f"{self.wms_cache_dir}/rasters/{folder}/geometries.json")
            )


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
