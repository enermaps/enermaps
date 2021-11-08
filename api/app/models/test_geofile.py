import copy
import json
import os
import shutil

import mapnik

from app.common import path
from app.common.projection import epsg_string_to_proj4
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
            },
            {
                "id": "FEATURE_ID",
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [],
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
            },
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
            self.assertTrue(
                os.path.exists(f"{self.wms_cache_dir}/vectors/42/projection.txt")
            )
            self.assertTrue(
                os.path.exists(f"{self.wms_cache_dir}/vectors/42/variables.json")
            )
            self.assertTrue(
                os.path.exists(f"{self.wms_cache_dir}/vectors/42/bbox.json")
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

    def testBboxFile(self):
        with self.flask_app.app_context():
            layer_name = "vector/42"

            geofile.save_vector_geojson(
                layer_name, copy.deepcopy(TestSaveVectorGeoJSON.GEOJSON)
            )

            with open(f"{self.wms_cache_dir}/vectors/42/bbox.json", "r") as f:
                bbox = json.load(f)

            self.assertTrue(isinstance(bbox, dict))
            self.assertTrue("left" in bbox)
            self.assertTrue("right" in bbox)
            self.assertTrue("bottom" in bbox)
            self.assertTrue("top" in bbox)

            self.assertAlmostEqual(bbox["left"], 7.4)
            self.assertAlmostEqual(bbox["right"], 7.4)
            self.assertAlmostEqual(bbox["bottom"], 46.0)
            self.assertAlmostEqual(bbox["top"], 46.0)


class TestSaveRasterProjection(BaseApiTest):
    def testFileCreation(self):
        with self.flask_app.app_context():
            layer_name = "raster/42"

            geofile.save_raster_projection(
                layer_name, epsg_string_to_proj4("EPSG:3035")
            )

            self.assertTrue(
                os.path.exists(f"{self.wms_cache_dir}/rasters/42/projection.txt")
            )

    def testFileCreationWithFullLayerName(self):
        with self.flask_app.app_context():
            layer_name = path.make_unique_layer_name(
                path.RASTER, 42, time_period="2015", variable="variable"
            )

            geofile.save_raster_projection(
                layer_name, epsg_string_to_proj4("EPSG:3035")
            )

            self.assertTrue(
                os.path.exists(f"{self.wms_cache_dir}/rasters/42/projection.txt")
            )

    def testFileContent(self):
        with self.flask_app.app_context():
            layer_name = "raster/42"

            projection = epsg_string_to_proj4("EPSG:3035")

            geofile.save_raster_projection(layer_name, projection)

            with open(f"{self.wms_cache_dir}/rasters/42/projection.txt", "r") as f:
                data = f.read()

            self.assertEqual(data, projection)


class TestSaveRasterGeometries(BaseApiTest):
    RASTERS = [
        {
            "fid": "FID1.tif",
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
        },
    ]

    def testSuccess(self):
        with self.flask_app.app_context():
            layer_name = path.make_unique_layer_name(
                path.RASTER, 42, time_period="2015", variable="variable"
            )

            geofile.save_raster_geometries(
                layer_name, copy.deepcopy(TestSaveRasterGeometries.RASTERS)
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
                    TestSaveRasterGeometries.RASTERS[0]["geometry"]["coordinates"][0][
                        i
                    ],
                )

            filename = f"{self.wms_cache_dir}/rasters/{folder}/bbox.json"
            self.assertTrue(os.path.exists(filename))

            with open(filename, "r") as f:
                bbox = json.load(f)

            self.assertTrue(isinstance(bbox, dict))
            self.assertTrue("left" in bbox)
            self.assertTrue("right" in bbox)
            self.assertTrue("bottom" in bbox)
            self.assertTrue("top" in bbox)

            self.assertAlmostEqual(bbox["left"], 10)
            self.assertAlmostEqual(bbox["right"], 20)
            self.assertAlmostEqual(bbox["bottom"], 30)
            self.assertAlmostEqual(bbox["top"], 40)

    def testFailureNoFeatures(self):
        with self.flask_app.app_context():
            layer_name = path.make_unique_layer_name(
                path.RASTER, 42, time_period="2015", variable="variable"
            )

            rasters = []

            geofile.save_raster_geometries(layer_name, rasters)

            folder = path.to_folder_path(layer_name)
            self.assertFalse(
                os.path.exists(f"{self.wms_cache_dir}/rasters/{folder}/geometries.json")
            )

            self.assertFalse(
                os.path.exists(f"{self.wms_cache_dir}/rasters/{folder}/bbox.json")
            )

    def testSuccessNoGeometry(self):
        with self.flask_app.app_context():
            layer_name = path.make_unique_layer_name(
                path.RASTER, 42, time_period="2015", variable="variable"
            )

            folder = path.to_folder_path(layer_name)

            raster_filename = self.get_testdata_path("hotmaps-cdd_curr_adapted.tif")

            os.makedirs(f"{self.wms_cache_dir}/rasters/{folder}")
            shutil.copy(
                raster_filename, f"{self.wms_cache_dir}/rasters/{folder}/FID1.tif"
            )

            rasters = copy.deepcopy(TestSaveRasterGeometries.RASTERS)
            rasters[0]["geometry"] = None

            geofile.save_raster_geometries(layer_name, rasters)

            filename = f"{self.wms_cache_dir}/rasters/{folder}/geometries.json"

            self.assertTrue(os.path.exists(filename))

            with open(filename, "r") as f:
                geometries = json.load(f)

            self.assertEqual(len(geometries), 1)
            self.assertTrue("FID1.tif" in geometries)

            self.assertTrue(geometries["FID1.tif"] is None)

            filename = f"{self.wms_cache_dir}/rasters/{folder}/bbox.json"
            self.assertTrue(os.path.exists(filename))

            with open(filename, "r") as f:
                bbox = json.load(f)

            self.assertTrue(isinstance(bbox, dict))
            self.assertTrue("left" in bbox)
            self.assertTrue("right" in bbox)
            self.assertTrue("bottom" in bbox)
            self.assertTrue("top" in bbox)

            self.assertAlmostEqual(bbox["left"], -23.541022392946928)
            self.assertAlmostEqual(bbox["right"], 60.231123578111784)
            self.assertAlmostEqual(bbox["bottom"], 24.772138781524273)
            self.assertAlmostEqual(bbox["top"], 64.20132131770235)

    def testSuccessNotPolygon(self):
        with self.flask_app.app_context():
            layer_name = path.make_unique_layer_name(
                path.RASTER, 42, time_period="2015", variable="variable"
            )

            folder = path.to_folder_path(layer_name)

            raster_filename = self.get_testdata_path("hotmaps-cdd_curr_adapted.tif")

            os.makedirs(f"{self.wms_cache_dir}/rasters/{folder}")
            shutil.copy(
                raster_filename, f"{self.wms_cache_dir}/rasters/{folder}/FID1.tif"
            )

            rasters = copy.deepcopy(TestSaveRasterGeometries.RASTERS)
            rasters[0]["geometry"]["type"] = "Point"

            geofile.save_raster_geometries(layer_name, rasters)

            filename = f"{self.wms_cache_dir}/rasters/{folder}/geometries.json"

            self.assertTrue(os.path.exists(filename))

            with open(filename, "r") as f:
                geometries = json.load(f)

            self.assertEqual(len(geometries), 1)
            self.assertTrue("FID1.tif" in geometries)

            self.assertTrue(geometries["FID1.tif"] is None)

            filename = f"{self.wms_cache_dir}/rasters/{folder}/geometries.json"

            self.assertTrue(os.path.exists(filename))

            with open(filename, "r") as f:
                geometries = json.load(f)

            self.assertEqual(len(geometries), 1)
            self.assertTrue("FID1.tif" in geometries)

            self.assertTrue(geometries["FID1.tif"] is None)

            filename = f"{self.wms_cache_dir}/rasters/{folder}/bbox.json"
            self.assertTrue(os.path.exists(filename))

            with open(filename, "r") as f:
                bbox = json.load(f)

            self.assertTrue(isinstance(bbox, dict))
            self.assertTrue("left" in bbox)
            self.assertTrue("right" in bbox)
            self.assertTrue("bottom" in bbox)
            self.assertTrue("top" in bbox)

            self.assertAlmostEqual(bbox["left"], -23.541022392946928)
            self.assertAlmostEqual(bbox["right"], 60.231123578111784)
            self.assertAlmostEqual(bbox["bottom"], 24.772138781524273)
            self.assertAlmostEqual(bbox["top"], 64.20132131770235)


class TestSaveRasterFile(BaseApiTest):
    def testSimple(self):
        with self.flask_app.app_context():
            raster_filename = self.get_testdata_path("hotmaps-cdd_curr_adapted.tif")
            with open(raster_filename, "rb") as f:
                content = f.read()

            self.assertTrue(geofile.save_raster_file("raster/42", "file.tif", content))

            storage_instance = storage.create("raster/42")
            self.assertTrue(
                os.path.exists(storage_instance.get_file_path("raster/42", "file.tif"))
            )

    def testWithSubFolders(self):
        with self.flask_app.app_context():
            raster_filename = self.get_testdata_path("hotmaps-cdd_curr_adapted.tif")
            with open(raster_filename, "rb") as f:
                content = f.read()

            self.assertTrue(
                geofile.save_raster_file("raster/42", "subfolder/file.tif", content)
            )

            storage_instance = storage.create("raster/42")
            self.assertTrue(
                os.path.exists(
                    storage_instance.get_file_path("raster/42", "subfolder/file.tif")
                )
            )


class TestSaveCMFile(BaseApiTest):
    def testSave(self):
        with self.flask_app.app_context():
            layer_name = "cm/some_name/01234567-0000-0000-0000-000000000000"

            raster_filename = self.get_testdata_path("hotmaps-cdd_curr_adapted.tif")
            with open(raster_filename, "rb") as f:
                content = f.read()

            self.assertTrue(geofile.save_cm_file(layer_name, "file.tif", content))

            storage_instance = storage.create(layer_name)
            self.assertTrue(
                os.path.exists(storage_instance.get_file_path(layer_name, "file.tif"))
            )
            self.assertTrue(
                os.path.exists(
                    storage_instance.get_projection_file(layer_name, "file.tif")
                )
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


class TestRasterLayerIntersectionsBase(BaseApiTest):
    def setUp(self):
        super().setUp()

        with self.flask_app.app_context():
            # Copy the raster dataset
            layer_name = path.make_unique_layer_name(path.RASTER, 42, "heat")
            storage_instance = storage.create(layer_name)

            os.makedirs(storage_instance.get_dir(layer_name))

            shutil.copy(
                self.get_testdata_path("hotmaps-cdd_curr_adapted.tif"),
                storage_instance.get_file_path(layer_name, "FID.tif"),
            )

            self.createGeometryFile(storage_instance.get_geometries_file(layer_name))

    def createGeometryFile(self, filename):
        pass


class TestRasterLayerIntersectionsWithoutGeometryFile(TestRasterLayerIntersectionsBase):
    def testIntersectsBoundingBox(self):
        with self.flask_app.app_context():
            layer_name = path.make_unique_layer_name(path.RASTER, 42, "heat")
            layer = geofile.load(layer_name)

            rasters = layer.get_rasters_in_bbox(
                mapnik.Box2d(40, 0, 60, 10), "EPSG:4326"
            )
            self.assertEqual(len(rasters), 0)

    def testIntersectsOneFeatureOnePolygon(self):
        with self.flask_app.app_context():
            layer_name = path.make_unique_layer_name(path.RASTER, 42, "heat")
            layer = geofile.load(layer_name)

            features = [
                {
                    "geometry": {
                        "coordinates": [[[5, 40], [8, 40], [8, 45], [5, 45], [5, 40]]]
                    }
                }
            ]

            rasters = layer.get_rasters_in_feature_list(features)
            self.assertEqual(len(rasters), 0)

    def testIntersectsOneFeatureTwoPolygons(self):
        with self.flask_app.app_context():
            layer_name = path.make_unique_layer_name(path.RASTER, 42, "heat")
            layer = geofile.load(layer_name)

            features = [
                {
                    "geometry": {
                        "coordinates": [
                            [[5, 40], [8, 40], [8, 45], [5, 45], [5, 40]],
                            [[5, 50], [8, 50], [8, 55], [5, 55], [5, 50]],
                        ]
                    }
                }
            ]

            rasters = layer.get_rasters_in_feature_list(features)
            self.assertEqual(len(rasters), 0)

    def testIntersectsTwoFeaturesOnePolygon(self):
        with self.flask_app.app_context():
            layer_name = path.make_unique_layer_name(path.RASTER, 42, "heat")
            layer = geofile.load(layer_name)

            features = [
                {
                    "geometry": {
                        "coordinates": [[[5, 40], [8, 40], [8, 45], [5, 45], [5, 40]]]
                    }
                },
                {
                    "geometry": {
                        "coordinates": [[[5, 50], [8, 50], [8, 55], [5, 55], [5, 50]]]
                    }
                },
            ]

            rasters = layer.get_rasters_in_feature_list(features)
            self.assertEqual(len(rasters), 0)


class TestRasterLayerIntersectionsWithoutCoordinatesInGeometryFile(
    TestRasterLayerIntersectionsBase
):
    def createGeometryFile(self, filename):
        data = {"FID.tif": None}

        with open(filename, "w") as f:
            json.dump(data, f)

    def testIntersectsBoundingBox(self):
        with self.flask_app.app_context():
            layer_name = path.make_unique_layer_name(path.RASTER, 42, "heat")
            layer = geofile.load(layer_name)

            rasters = layer.get_rasters_in_bbox(
                mapnik.Box2d(40, 0, 60, 10), "EPSG:4326"
            )
            self.assertEqual(len(rasters), 1)
            self.assertEqual(
                rasters[0],
                (
                    "FID.tif",
                    layer.storage.get_file_path(layer_name, "FID.tif"),
                ),
            )

    def testIntersectsOneFeatureOnePolygon(self):
        with self.flask_app.app_context():
            layer_name = path.make_unique_layer_name(path.RASTER, 42, "heat")
            layer = geofile.load(layer_name)

            features = [
                {
                    "geometry": {
                        "coordinates": [[[5, 40], [8, 40], [8, 45], [5, 45], [5, 40]]]
                    }
                }
            ]

            rasters = layer.get_rasters_in_feature_list(features)
            self.assertEqual(len(rasters), 1)
            self.assertEqual(
                rasters[0],
                (
                    "FID.tif",
                    layer.storage.get_file_path(layer_name, "FID.tif"),
                ),
            )

    def testIntersectsOneFeatureTwoPolygons(self):
        with self.flask_app.app_context():
            layer_name = path.make_unique_layer_name(path.RASTER, 42, "heat")
            layer = geofile.load(layer_name)

            features = [
                {
                    "geometry": {
                        "coordinates": [
                            [[5, 40], [8, 40], [8, 45], [5, 45], [5, 40]],
                            [[5, 50], [8, 50], [8, 55], [5, 55], [5, 50]],
                        ]
                    }
                }
            ]

            rasters = layer.get_rasters_in_feature_list(features)
            self.assertEqual(len(rasters), 1)
            self.assertEqual(
                rasters[0],
                (
                    "FID.tif",
                    layer.storage.get_file_path(layer_name, "FID.tif"),
                ),
            )

    def testIntersectsOneFeatureTwoPolygons2(self):
        with self.flask_app.app_context():
            layer_name = path.make_unique_layer_name(path.RASTER, 42, "heat")
            layer = geofile.load(layer_name)

            features = [
                {
                    "geometry": {
                        "coordinates": [
                            [[-70, 40], [-60, 40], [-60, 45], [-70, 45], [-70, 40]],
                            [[5, 50], [8, 50], [8, 55], [5, 55], [5, 50]],
                        ]
                    }
                }
            ]

            rasters = layer.get_rasters_in_feature_list(features)
            self.assertEqual(len(rasters), 1)
            self.assertEqual(
                rasters[0],
                (
                    "FID.tif",
                    layer.storage.get_file_path(layer_name, "FID.tif"),
                ),
            )

    def testIntersectsTwoFeaturesOnePolygon(self):
        with self.flask_app.app_context():
            layer_name = path.make_unique_layer_name(path.RASTER, 42, "heat")
            layer = geofile.load(layer_name)

            features = [
                {
                    "geometry": {
                        "coordinates": [[[5, 40], [8, 40], [8, 45], [5, 45], [5, 40]]]
                    }
                },
                {
                    "geometry": {
                        "coordinates": [[[5, 50], [8, 50], [8, 55], [5, 55], [5, 50]]]
                    }
                },
            ]

            rasters = layer.get_rasters_in_feature_list(features)
            self.assertEqual(len(rasters), 1)
            self.assertEqual(
                rasters[0],
                (
                    "FID.tif",
                    layer.storage.get_file_path(layer_name, "FID.tif"),
                ),
            )

    def testIntersectsTwoFeaturesOnePolygon2(self):
        with self.flask_app.app_context():
            layer_name = path.make_unique_layer_name(path.RASTER, 42, "heat")
            layer = geofile.load(layer_name)

            features = [
                {
                    "geometry": {
                        "coordinates": [
                            [[-70, 40], [-60, 40], [-60, 45], [-70, 45], [-70, 40]]
                        ]
                    }
                },
                {
                    "geometry": {
                        "coordinates": [[[5, 50], [8, 50], [8, 55], [5, 55], [5, 50]]]
                    }
                },
            ]

            rasters = layer.get_rasters_in_feature_list(features)
            self.assertEqual(len(rasters), 1)
            self.assertEqual(
                rasters[0],
                (
                    "FID.tif",
                    layer.storage.get_file_path(layer_name, "FID.tif"),
                ),
            )


class TestRasterLayerIntersections(
    TestRasterLayerIntersectionsWithoutCoordinatesInGeometryFile
):
    def createGeometryFile(self, filename):
        data = {"FID.tif": [[0, 60], [10, 60], [10, 30], [0, 30], [0, 60]]}

        with open(filename, "w") as f:
            json.dump(data, f)

    def testNotIntersectsBoundingBox(self):
        with self.flask_app.app_context():
            layer_name = path.make_unique_layer_name(path.RASTER, 42, "heat")
            layer = geofile.load(layer_name)

            rasters = layer.get_rasters_in_bbox(
                mapnik.Box2d(40, -70, 60, -60), "EPSG:4326"
            )
            self.assertEqual(len(rasters), 0)

    def testNotIntersectsOneFeatureOnePolygon(self):
        with self.flask_app.app_context():
            layer_name = path.make_unique_layer_name(path.RASTER, 42, "heat")
            layer = geofile.load(layer_name)

            features = [
                {
                    "geometry": {
                        "coordinates": [
                            [[-70, 40], [-60, 40], [-60, 45], [-70, 45], [-70, 40]]
                        ]
                    }
                }
            ]

            rasters = layer.get_rasters_in_feature_list(features)
            self.assertEqual(len(rasters), 0)

    def testNotIntersectsOneFeatureTwoPolygons(self):
        with self.flask_app.app_context():
            layer_name = path.make_unique_layer_name(path.RASTER, 42, "heat")
            layer = geofile.load(layer_name)

            features = [
                {
                    "geometry": {
                        "coordinates": [
                            [[-70, 40], [-60, 40], [-60, 45], [-70, 45], [-70, 40]],
                            [[-70, 50], [-60, 50], [-60, 55], [-70, 55], [-70, 50]],
                        ]
                    }
                }
            ]

            rasters = layer.get_rasters_in_feature_list(features)
            self.assertEqual(len(rasters), 0)

    def testNotIntersectsTwoFeaturesOnePolygon(self):
        with self.flask_app.app_context():
            layer_name = path.make_unique_layer_name(path.RASTER, 42, "heat")
            layer = geofile.load(layer_name)

            features = [
                {
                    "geometry": {
                        "coordinates": [
                            [[-70, 40], [-60, 40], [-60, 45], [-70, 45], [-70, 40]]
                        ]
                    }
                },
                {
                    "geometry": {
                        "coordinates": [
                            [[-70, 50], [-60, 50], [-60, 55], [-70, 55], [-70, 50]]
                        ]
                    }
                },
            ]

            rasters = layer.get_rasters_in_feature_list(features)
            self.assertEqual(len(rasters), 0)


class TestRasterLayerDataAndMapnikBase(BaseApiTest):
    def setUp(self):
        super().setUp()

        with self.flask_app.app_context():
            # Copy the raster dataset
            layer_name = self.getLayerName()
            storage_instance = storage.create(layer_name)

            os.makedirs(storage_instance.get_dir(layer_name))

            shutil.copy(
                self.get_testdata_path("hotmaps-cdd_curr_adapted.tif"),
                storage_instance.get_file_path(layer_name, "FID.tif"),
            )

            shutil.copy(
                storage_instance.get_file_path(layer_name, "FID.tif"),
                storage_instance.get_file_path(layer_name, "FID2.tif"),
            )

            self.createGeometryFile(storage_instance.get_geometries_file(layer_name))

    def getLayerName(self):
        pass

    def createGeometryFile(self, filename):
        pass


class TestCMLayerDataAndMapnikWithoutGeometryFile(TestRasterLayerDataAndMapnikBase):
    def setUp(self):
        super().setUp()

        with self.flask_app.app_context():
            layer_name = self.getLayerName()
            storage_instance = storage.create(layer_name)

            projection = epsg_string_to_proj4(
                self.flask_app.config["RASTER_PROJECTION_SYSTEM"]
            )

            with open(storage_instance.get_file_path(layer_name, "FID.prj"), "w") as f:
                f.write(projection)

            with open(storage_instance.get_file_path(layer_name, "FID2.prj"), "w") as f:
                f.write(projection)

    def getLayerName(self):
        return path.make_unique_layer_name(
            path.CM, "mock_cm", task_id="01234567-0000-0000-0000-000000000000"
        )

    def testDataWithBoundingBox(self):
        with self.flask_app.app_context():
            layer_name = self.getLayerName()
            layer = geofile.load(layer_name)

            data = layer.get_data_for_bounding_box(
                mapnik.Box2d(40, 0, 60, 10), "EPSG:4326"
            )

            self.assertEqual(len(data), 2)

    def testDataWithoutBoundingBox(self):
        with self.flask_app.app_context():
            layer_name = self.getLayerName()
            layer = geofile.load(layer_name)

            data = layer.get_data_for_bounding_box(None, None)
            self.assertEqual(len(data), 2)

    def testMapnikWithData(self):
        with self.flask_app.app_context():
            layer_name = self.getLayerName()
            layer = geofile.load(layer_name)

            storage_instance = storage.create(layer_name)

            data = [("FID.tif", storage_instance.get_file_path(layer_name, "FID.tif"))]

            layers = layer.as_mapnik_layers(data)
            self.assertEqual(len(layers), 1)

    def testMapnikWithMultipleData(self):
        with self.flask_app.app_context():
            layer_name = self.getLayerName()
            layer = geofile.load(layer_name)

            storage_instance = storage.create(layer_name)

            data = [
                ("FID.tif", storage_instance.get_file_path(layer_name, "FID.tif")),
                ("FID2.tif", storage_instance.get_file_path(layer_name, "FID.tif")),
            ]

            layers = layer.as_mapnik_layers(data)
            self.assertEqual(len(layers), 2)

    def testMapnikWithoutData(self):
        with self.flask_app.app_context():
            layer_name = self.getLayerName()
            layer = geofile.load(layer_name)

            layers = layer.as_mapnik_layers()
            self.assertEqual(len(layers), 2)

    def testMapnikWithInvalidData(self):
        with self.flask_app.app_context():
            layer_name = self.getLayerName()
            layer = geofile.load(layer_name)

            storage_instance = storage.create(layer_name)

            data = [
                ("FID.tif", storage_instance.get_file_path(layer_name, "unknown.tif"))
            ]

            layers = layer.as_mapnik_layers(data)
            self.assertEqual(len(layers), 0)


class TestRasterLayerDataAndMapnikWithoutGeometryFile(TestRasterLayerDataAndMapnikBase):
    def getLayerName(self):
        return path.make_unique_layer_name(path.RASTER, 42, variable="heat")

    def testDataWithBoundingBox(self):
        with self.flask_app.app_context():
            layer_name = self.getLayerName()
            layer = geofile.load(layer_name)

            data = layer.get_data_for_bounding_box(
                mapnik.Box2d(40, 0, 60, 10), "EPSG:4326"
            )

            self.assertEqual(len(data), 0)

    def testDataWithoutBoundingBox(self):
        with self.flask_app.app_context():
            layer_name = self.getLayerName()
            layer = geofile.load(layer_name)

            data = layer.get_data_for_bounding_box(None, None)
            self.assertEqual(len(data), 0)

    def testMapnikWithData(self):
        with self.flask_app.app_context():
            layer_name = self.getLayerName()
            layer = geofile.load(layer_name)

            storage_instance = storage.create(layer_name)

            data = [("FID.tif", storage_instance.get_file_path(layer_name, "FID.tif"))]

            layers = layer.as_mapnik_layers(data)
            self.assertEqual(len(layers), 1)

    def testMapnikWithMultipleData(self):
        with self.flask_app.app_context():
            layer_name = self.getLayerName()
            layer = geofile.load(layer_name)

            storage_instance = storage.create(layer_name)

            data = [
                ("FID.tif", storage_instance.get_file_path(layer_name, "FID.tif")),
                ("FID2.tif", storage_instance.get_file_path(layer_name, "FID.tif")),
            ]

            layers = layer.as_mapnik_layers(data)
            self.assertEqual(len(layers), 2)

    def testMapnikWithoutData(self):
        with self.flask_app.app_context():
            layer_name = self.getLayerName()
            layer = geofile.load(layer_name)

            layers = layer.as_mapnik_layers()
            self.assertEqual(len(layers), 0)

    def testMapnikWithInvalidData(self):
        with self.flask_app.app_context():
            layer_name = self.getLayerName()
            layer = geofile.load(layer_name)

            storage_instance = storage.create(layer_name)

            data = [
                ("FID.tif", storage_instance.get_file_path(layer_name, "unknown.tif"))
            ]

            layers = layer.as_mapnik_layers(data)
            self.assertEqual(len(layers), 0)


class TestRasterLayerDataAndMapnikWithoutCoordinatesInGeometryFile(
    TestRasterLayerDataAndMapnikBase
):
    def getLayerName(self):
        return path.make_unique_layer_name(path.RASTER, 42, variable="heat")

    def createGeometryFile(self, filename):
        data = {"FID.tif": None}

        with open(filename, "w") as f:
            json.dump(data, f)

    def testDataWithBoundingBox(self):
        with self.flask_app.app_context():
            layer_name = self.getLayerName()
            layer = geofile.load(layer_name)

            data = layer.get_data_for_bounding_box(
                mapnik.Box2d(40, 0, 60, 10), "EPSG:4326"
            )

            self.assertEqual(len(data), 1)

    def testDataWithoutBoundingBox(self):
        with self.flask_app.app_context():
            layer_name = self.getLayerName()
            layer = geofile.load(layer_name)

            data = layer.get_data_for_bounding_box(None, None)
            self.assertEqual(len(data), 1)

    def testMapnikWithData(self):
        with self.flask_app.app_context():
            layer_name = self.getLayerName()
            layer = geofile.load(layer_name)

            storage_instance = storage.create(layer_name)

            data = [("FID.tif", storage_instance.get_file_path(layer_name, "FID.tif"))]

            layers = layer.as_mapnik_layers(data)
            self.assertEqual(len(layers), 1)

    def testMapnikWithMultipleData(self):
        with self.flask_app.app_context():
            layer_name = self.getLayerName()
            layer = geofile.load(layer_name)

            storage_instance = storage.create(layer_name)

            data = [
                ("FID.tif", storage_instance.get_file_path(layer_name, "FID.tif")),
                ("FID2.tif", storage_instance.get_file_path(layer_name, "FID.tif")),
            ]

            layers = layer.as_mapnik_layers(data)
            self.assertEqual(len(layers), 2)

    def testMapnikWithoutData(self):
        with self.flask_app.app_context():
            layer_name = self.getLayerName()
            layer = geofile.load(layer_name)

            layers = layer.as_mapnik_layers()
            self.assertEqual(len(layers), 1)

    def testMapnikWithInvalidData(self):
        with self.flask_app.app_context():
            layer_name = self.getLayerName()
            layer = geofile.load(layer_name)

            storage_instance = storage.create(layer_name)

            data = [
                ("FID.tif", storage_instance.get_file_path(layer_name, "unknown.tif"))
            ]

            layers = layer.as_mapnik_layers(data)
            self.assertEqual(len(layers), 0)


class TestRasterLayerDataAndMapnik(
    TestRasterLayerDataAndMapnikWithoutCoordinatesInGeometryFile
):
    def createGeometryFile(self, filename):
        data = {"FID.tif": [[0, 60], [10, 60], [10, 30], [0, 30], [0, 60]]}

        with open(filename, "w") as f:
            json.dump(data, f)

    def testDataNotIntersectsBoundingBox(self):
        with self.flask_app.app_context():
            layer_name = path.make_unique_layer_name(path.RASTER, 42, "heat")
            layer = geofile.load(layer_name)

            data = layer.get_data_for_bounding_box(
                mapnik.Box2d(40, -70, 60, -60), "EPSG:4326"
            )

            self.assertEqual(len(data), 0)
