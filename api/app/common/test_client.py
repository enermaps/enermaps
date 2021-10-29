import copy
import json
import os
from unittest.mock import Mock, patch

from app.common import client, datasets, path
from app.common.test import BaseApiTest


class Response(object):
    def __init__(self, content):
        self.content = content

    def json(self):
        return json.loads(self.content)


def setupResponse(response):
    ctx_mgr = Mock()
    ctx_mgr.__enter__ = Mock(return_value=response)
    ctx_mgr.__exit__ = Mock(return_value=None)
    return ctx_mgr


def setupResponseWithSideEffect(responses):
    ctx_mgr = Mock()
    ctx_mgr.__enter__ = Mock(side_effect=responses)
    ctx_mgr.__exit__ = Mock(return_value=None)
    return ctx_mgr


class TTLHashTest(BaseApiTest):
    @patch(
        "time.time",
    )
    def testSameHash(self, time_fct):
        time_fct.return_value = 1000000
        hash1 = client.get_ttl_hash()

        time_fct.return_value = 1000005
        hash2 = client.get_ttl_hash()

        self.assertEqual(hash1, hash2)

    @patch(
        "time.time",
    )
    def testDifferentHashes(self, time_fct):
        time_fct.return_value = 1000000
        hash1 = client.get_ttl_hash()

        time_fct.return_value = 1000015
        hash2 = client.get_ttl_hash()

        self.assertNotEqual(hash1, hash2)


class DatasetListTest(BaseApiTest):

    DATASETS = [
        {
            "ds_id": 1,
            "is_raster": True,
        },
        {
            "ds_id": 2,
            "is_raster": False,
        },
    ]

    def setUp(self):
        super().setUp()
        os.makedirs(os.path.join(self.wms_cache_dir, "rasters", "1"))

    @patch("requests.get")
    def testWithoutFiltering(self, get_mock):
        with self.flask_app.app_context():
            get_mock.return_value = setupResponse(
                Response(json.dumps(DatasetListTest.DATASETS))
            )

            datasets = client.get_dataset_list(disable_filtering=True)

            self.assertEqual(len(get_mock.call_args.args), 1)
            self.assertEqual(get_mock.call_args.args[0], "dataset_list")

            self.assertEqual(len(get_mock.call_args.kwargs), 0)

            self.assertEqual(datasets, DatasetListTest.DATASETS)

    @patch("requests.get")
    def testWithFiltering(self, get_mock):
        with self.flask_app.app_context():
            get_mock.return_value = setupResponse(
                Response(json.dumps(DatasetListTest.DATASETS))
            )

            datasets = client.get_dataset_list()

            self.assertEqual(len(get_mock.call_args.args), 1)
            self.assertEqual(get_mock.call_args.args[0], "dataset_list")

            self.assertEqual(len(get_mock.call_args.kwargs), 0)

            self.assertEqual(len(datasets), 1)
            self.assertEqual(datasets[0], DatasetListTest.DATASETS[0])

    @patch("requests.get")
    def testFailure(self, get_mock):
        with self.flask_app.app_context():
            get_mock.side_effect = Exception()

            datasets = client.get_dataset_list()
            self.assertEqual(len(datasets), 0)


class ParametersTest(BaseApiTest):

    PARAMETERS = {
        "end_at": None,
        "parameters": {
            "end_at": None,
            "fields": [],
            "levels": [],
            "is_tiled": False,
            "start_at": None,
            "is_raster": False,
            "variables": [
                "var1",
            ],
            "time_periods": [],
            "temporal_granularity": None,
        },
        "default_parameters": {},
    }

    @patch("requests.get")
    def testSuccess(self, get_mock):
        with self.flask_app.app_context():
            get_mock.return_value = setupResponse(
                Response(json.dumps(ParametersTest.PARAMETERS))
            )

            parameters = client.get_parameters(1)

            self.assertEqual(len(get_mock.call_args.args), 1)
            self.assertEqual(get_mock.call_args.args[0], "rpc/enermaps_get_parameters")

            self.assertEqual(len(get_mock.call_args.kwargs), 2)
            self.assertTrue("headers" in get_mock.call_args.kwargs)
            self.assertTrue("params" in get_mock.call_args.kwargs)
            self.assertTrue("Authorization" in get_mock.call_args.kwargs["headers"])
            self.assertTrue("id" in get_mock.call_args.kwargs["params"])
            self.assertEqual(get_mock.call_args.kwargs["params"]["id"], 1)

            self.assertEqual(parameters, datasets.convert(ParametersTest.PARAMETERS))

    @patch("requests.get")
    def testFailure(self, get_mock):
        with self.flask_app.app_context():
            get_mock.side_effect = Exception()

            parameters = client.get_parameters(1)
            self.assertTrue(parameters is None)


class AreasTest(BaseApiTest):
    def testSuccess(self):
        with self.flask_app.app_context():
            areas = client.get_areas()

            self.assertEqual(len(areas), 5)
            for area in areas:
                self.assertTrue("id" in area)
                self.assertTrue("title" in area)


class RasterFileTest(BaseApiTest):

    RASTER_CONTENT = b"this is a raster file"

    @patch("requests.get")
    def testSuccess(self, get_mock):
        with self.flask_app.app_context():
            get_mock.return_value = setupResponse(
                Response(RasterFileTest.RASTER_CONTENT)
            )

            content = client.get_raster_file(1, "FID.tif")

            self.assertEqual(len(get_mock.call_args.args), 1)
            self.assertEqual(get_mock.call_args.args[0], "1/FID.tif")

            self.assertEqual(len(get_mock.call_args.kwargs), 1)
            self.assertTrue("stream" in get_mock.call_args.kwargs)
            self.assertTrue(get_mock.call_args.kwargs["stream"])

            self.assertEqual(content, RasterFileTest.RASTER_CONTENT)

    @patch("requests.get")
    def testFailure(self, get_mock):
        with self.flask_app.app_context():
            get_mock.side_effect = Exception()

            content = client.get_raster_file(1, "FID.tif")
            self.assertTrue(content is None)


class GeoJSONTest(BaseApiTest):

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
        ],
    }

    PARAMETERS = {
        "end_at": None,
        "parameters": {
            "end_at": None,
            "fields": [],
            "levels": [],
            "is_tiled": False,
            "start_at": None,
            "is_raster": False,
            "variables": [],
            "time_periods": [],
            "temporal_granularity": None,
        },
        "default_parameters": {},
    }

    PARAMETERS_VARIABLE = {
        "end_at": None,
        "parameters": {
            "end_at": None,
            "fields": [],
            "levels": [],
            "is_tiled": False,
            "start_at": None,
            "is_raster": False,
            "variables": [
                "var1",
            ],
            "time_periods": [],
            "temporal_granularity": None,
        },
        "default_parameters": {},
    }

    PARAMETERS_DEFAULT_VARIABLE = {
        "end_at": None,
        "parameters": {
            "end_at": None,
            "fields": [],
            "levels": [],
            "is_tiled": False,
            "start_at": None,
            "is_raster": False,
            "variables": [
                "var1",
            ],
            "time_periods": [],
            "temporal_granularity": None,
        },
        "default_parameters": {"variable": "var1"},
    }

    PARAMETERS_DEFAULT_VARIABLE2 = {
        "end_at": None,
        "parameters": {
            "end_at": None,
            "fields": [],
            "levels": [],
            "is_tiled": False,
            "start_at": None,
            "is_raster": False,
            "variables": [
                "var1",
                "var2",
            ],
            "time_periods": [],
            "temporal_granularity": None,
        },
        "default_parameters": {"variable": "var2"},
    }

    PARAMETERS_TIME_PERIOD = {
        "end_at": None,
        "parameters": {
            "end_at": None,
            "fields": [],
            "levels": [],
            "is_tiled": False,
            "start_at": None,
            "is_raster": False,
            "variables": [],
            "time_periods": ["2015"],
            "temporal_granularity": None,
        },
        "default_parameters": {},
    }

    PARAMETERS_TIME_PERIOD_WITH_MONTH = {
        "end_at": None,
        "parameters": {
            "end_at": None,
            "fields": [],
            "levels": [],
            "is_tiled": False,
            "start_at": None,
            "is_raster": False,
            "variables": [],
            "time_periods": ["2015-05"],
            "temporal_granularity": None,
        },
        "default_parameters": {},
    }

    PARAMETERS_NONE_TIME_PERIOD = {
        "end_at": None,
        "parameters": {
            "end_at": None,
            "fields": [],
            "levels": [],
            "is_tiled": False,
            "start_at": None,
            "is_raster": False,
            "variables": [],
            "time_periods": ["2015", "None"],
            "temporal_granularity": None,
        },
        "default_parameters": {},
    }

    PARAMETERS_MONTH_TIME_PERIOD = {
        "end_at": None,
        "parameters": {
            "end_at": None,
            "fields": [],
            "levels": [],
            "is_tiled": False,
            "start_at": "2015-01-01 00:00",
            "is_raster": False,
            "variables": [],
            "time_periods": ["07"],
            "temporal_granularity": None,
        },
        "default_parameters": {},
    }

    PARAMETERS_DEFAULT_TIME_PERIOD = {
        "end_at": None,
        "parameters": {
            "end_at": None,
            "fields": [],
            "levels": [],
            "is_tiled": False,
            "start_at": None,
            "is_raster": False,
            "variables": [],
            "time_periods": ["2015"],
            "temporal_granularity": None,
        },
        "default_parameters": {"start_at": "2015-01-01"},
    }

    PARAMETERS_DEFAULT_TIME_PERIOD2 = {
        "end_at": None,
        "parameters": {
            "end_at": None,
            "fields": [],
            "levels": [],
            "is_tiled": False,
            "start_at": None,
            "is_raster": False,
            "variables": [],
            "time_periods": ["2015", "2016"],
            "temporal_granularity": None,
        },
        "default_parameters": {"start_at": "2016-01-01"},
    }

    PARAMETERS_DEFAULT_FIELDS = {
        "end_at": None,
        "parameters": {
            "end_at": None,
            "fields": [],
            "levels": [],
            "is_tiled": False,
            "start_at": None,
            "is_raster": False,
            "variables": [],
            "time_periods": [],
            "temporal_granularity": None,
        },
        "default_parameters": {"fields": {"field1": "value"}},
    }

    PARAMETERS_DEFAULT_EMPTY_FIELDS = {
        "end_at": None,
        "parameters": {
            "end_at": None,
            "fields": [],
            "levels": [],
            "is_tiled": False,
            "start_at": None,
            "is_raster": False,
            "variables": [],
            "time_periods": [],
            "temporal_granularity": None,
        },
        "default_parameters": {"fields": {}},
    }

    PARAMETERS_DEFAULT_LEVEL = {
        "end_at": None,
        "parameters": {
            "end_at": None,
            "fields": [],
            "levels": [],
            "is_tiled": False,
            "start_at": None,
            "is_raster": False,
            "variables": [],
            "time_periods": [],
            "temporal_granularity": None,
        },
        "default_parameters": {"level": "{country}"},
    }

    PARAMETERS_DEFAULT_INTERSECTING = {
        "end_at": None,
        "parameters": {
            "end_at": None,
            "fields": [],
            "levels": [],
            "is_tiled": False,
            "start_at": None,
            "is_raster": False,
            "variables": [],
            "time_periods": [],
            "temporal_granularity": None,
        },
        "default_parameters": {
            "intersecting": (
                "POLYGON((2.29 48.88,2.29 48.87,2.3 48.87,2.3 48.88,2.29 48.88))"
            )
        },
    }

    def checkCallArguments(self, get_mock):
        self.assertEqual(get_mock.call_count, 1)

        self.assertEqual(len(get_mock.call_args.args), 1)
        self.assertEqual(get_mock.call_args.args[0], "rpc/enermaps_query_geojson")

        self.assertEqual(len(get_mock.call_args.kwargs), 2)

        self.assertTrue("headers" in get_mock.call_args.kwargs)
        self.assertTrue("Authorization" in get_mock.call_args.kwargs["headers"])

        self.assertTrue("params" in get_mock.call_args.kwargs)
        self.assertTrue("parameters" in get_mock.call_args.kwargs["params"])
        self.assertTrue("row_offset" in get_mock.call_args.kwargs["params"])
        self.assertTrue("row_limit" in get_mock.call_args.kwargs["params"])
        self.assertEqual(get_mock.call_args.kwargs["params"]["row_offset"], 0)
        self.assertEqual(get_mock.call_args.kwargs["params"]["row_limit"], 1000)

        return json.loads(get_mock.call_args.kwargs["params"]["parameters"])

    @patch("requests.get")
    @patch(
        "app.common.client.get_parameters",
        new=Mock(return_value=datasets.convert(PARAMETERS)),
    )
    def testSimple(self, get_mock):
        with self.flask_app.app_context():
            get_mock.return_value = setupResponse(
                Response(json.dumps(GeoJSONTest.GEOJSON))
            )

            layer_name = path.make_unique_layer_name(path.VECTOR, 1)
            geojson = client.get_geojson(layer_name)

            req_parameters = self.checkCallArguments(get_mock)

            self.assertTrue("data.ds_id" in req_parameters)
            self.assertEqual(req_parameters["data.ds_id"], 1)

            self.assertTrue("variable" not in req_parameters)
            self.assertTrue("start_at" not in req_parameters)
            self.assertTrue("intersecting" not in req_parameters)
            self.assertTrue("fields" not in req_parameters)
            self.assertTrue("level" not in req_parameters)

            self.assertEqual(geojson, GeoJSONTest.GEOJSON)

    @patch("requests.get")
    @patch(
        "app.common.client.get_parameters",
        new=Mock(return_value=datasets.convert(PARAMETERS_VARIABLE)),
    )
    def testWithVariable(self, get_mock):
        with self.flask_app.app_context():
            get_mock.return_value = setupResponse(
                Response(json.dumps(GeoJSONTest.GEOJSON))
            )

            layer_name = path.make_unique_layer_name(path.VECTOR, 1, variable="var1")
            geojson = client.get_geojson(layer_name)

            req_parameters = self.checkCallArguments(get_mock)

            self.assertTrue("data.ds_id" in req_parameters)
            self.assertEqual(req_parameters["data.ds_id"], 1)

            self.assertTrue("variable" in req_parameters)
            self.assertEqual(req_parameters["variable"], "'var1'")

            self.assertTrue("start_at" not in req_parameters)
            self.assertTrue("intersecting" not in req_parameters)
            self.assertTrue("fields" not in req_parameters)
            self.assertTrue("level" not in req_parameters)

            self.assertEqual(geojson, GeoJSONTest.GEOJSON)

    @patch("requests.get")
    @patch(
        "app.common.client.get_parameters",
        new=Mock(return_value=datasets.convert(PARAMETERS_DEFAULT_VARIABLE)),
    )
    def testWithDefaultVariable(self, get_mock):
        with self.flask_app.app_context():
            get_mock.return_value = setupResponse(
                Response(json.dumps(GeoJSONTest.GEOJSON))
            )

            layer_name = path.make_unique_layer_name(path.VECTOR, 1)
            geojson = client.get_geojson(layer_name)

            req_parameters = self.checkCallArguments(get_mock)

            self.assertTrue("data.ds_id" in req_parameters)
            self.assertEqual(req_parameters["data.ds_id"], 1)

            self.assertTrue("variable" in req_parameters)
            self.assertEqual(req_parameters["variable"], "'var1'")

            self.assertTrue("start_at" not in req_parameters)
            self.assertTrue("intersecting" not in req_parameters)
            self.assertTrue("fields" not in req_parameters)
            self.assertTrue("level" not in req_parameters)

            self.assertEqual(geojson, GeoJSONTest.GEOJSON)

    @patch("requests.get")
    @patch(
        "app.common.client.get_parameters",
        new=Mock(return_value=datasets.convert(PARAMETERS_DEFAULT_VARIABLE2)),
    )
    def testWithVariableOverridingDefault(self, get_mock):
        with self.flask_app.app_context():
            get_mock.return_value = setupResponse(
                Response(json.dumps(GeoJSONTest.GEOJSON))
            )

            layer_name = path.make_unique_layer_name(path.VECTOR, 1, variable="var1")
            geojson = client.get_geojson(layer_name)

            req_parameters = self.checkCallArguments(get_mock)

            self.assertTrue("data.ds_id" in req_parameters)
            self.assertEqual(req_parameters["data.ds_id"], 1)

            self.assertTrue("variable" in req_parameters)
            self.assertEqual(req_parameters["variable"], "'var1'")

            self.assertTrue("start_at" not in req_parameters)
            self.assertTrue("intersecting" not in req_parameters)
            self.assertTrue("fields" not in req_parameters)
            self.assertTrue("level" not in req_parameters)

            self.assertEqual(geojson, GeoJSONTest.GEOJSON)

    @patch("requests.get")
    @patch(
        "app.common.client.get_parameters",
        new=Mock(return_value=datasets.convert(PARAMETERS_TIME_PERIOD)),
    )
    def testWithTimePeriod(self, get_mock):
        with self.flask_app.app_context():
            get_mock.return_value = setupResponse(
                Response(json.dumps(GeoJSONTest.GEOJSON))
            )

            layer_name = path.make_unique_layer_name(path.VECTOR, 1, time_period="2015")
            geojson = client.get_geojson(layer_name)

            req_parameters = self.checkCallArguments(get_mock)

            self.assertTrue("data.ds_id" in req_parameters)
            self.assertEqual(req_parameters["data.ds_id"], 1)

            self.assertTrue("start_at" in req_parameters)
            self.assertEqual(req_parameters["start_at"], "'2015-01-01'")

            self.assertTrue("variable" not in req_parameters)
            self.assertTrue("intersecting" not in req_parameters)
            self.assertTrue("fields" not in req_parameters)
            self.assertTrue("level" not in req_parameters)

            self.assertEqual(geojson, GeoJSONTest.GEOJSON)

    @patch("requests.get")
    @patch(
        "app.common.client.get_parameters",
        new=Mock(return_value=datasets.convert(PARAMETERS_TIME_PERIOD_WITH_MONTH)),
    )
    def testWithTimePeriodWithMonth(self, get_mock):
        with self.flask_app.app_context():
            get_mock.return_value = setupResponse(
                Response(json.dumps(GeoJSONTest.GEOJSON))
            )

            layer_name = path.make_unique_layer_name(
                path.VECTOR, 1, time_period="2015-05"
            )
            geojson = client.get_geojson(layer_name)

            req_parameters = self.checkCallArguments(get_mock)

            self.assertTrue("data.ds_id" in req_parameters)
            self.assertEqual(req_parameters["data.ds_id"], 1)

            self.assertTrue("start_at" in req_parameters)
            self.assertEqual(req_parameters["start_at"], "'2015-05-01'")

            self.assertTrue("variable" not in req_parameters)
            self.assertTrue("intersecting" not in req_parameters)
            self.assertTrue("fields" not in req_parameters)
            self.assertTrue("level" not in req_parameters)

            self.assertEqual(geojson, GeoJSONTest.GEOJSON)

    @patch("requests.get")
    @patch(
        "app.common.client.get_parameters",
        new=Mock(return_value=datasets.convert(PARAMETERS_NONE_TIME_PERIOD)),
    )
    def testWithNoneTimePeriod(self, get_mock):
        with self.flask_app.app_context():
            get_mock.return_value = setupResponse(
                Response(json.dumps(GeoJSONTest.GEOJSON))
            )

            layer_name = path.make_unique_layer_name(path.VECTOR, 1, time_period="None")
            geojson = client.get_geojson(layer_name)

            req_parameters = self.checkCallArguments(get_mock)

            self.assertTrue("data.ds_id" in req_parameters)
            self.assertEqual(req_parameters["data.ds_id"], 1)

            self.assertTrue("start_at" in req_parameters)
            self.assertTrue(req_parameters["start_at"] is None)

            self.assertTrue("variable" not in req_parameters)
            self.assertTrue("intersecting" not in req_parameters)
            self.assertTrue("fields" not in req_parameters)
            self.assertTrue("level" not in req_parameters)

            self.assertEqual(geojson, GeoJSONTest.GEOJSON)

    @patch("requests.get")
    @patch(
        "app.common.client.get_parameters",
        new=Mock(return_value=datasets.convert(PARAMETERS_MONTH_TIME_PERIOD)),
    )
    def testWithMonthTimePeriod(self, get_mock):
        with self.flask_app.app_context():
            get_mock.return_value = setupResponse(
                Response(json.dumps(GeoJSONTest.GEOJSON))
            )

            layer_name = path.make_unique_layer_name(path.VECTOR, 1, time_period="07")
            geojson = client.get_geojson(layer_name)

            req_parameters = self.checkCallArguments(get_mock)

            self.assertTrue("data.ds_id" in req_parameters)
            self.assertEqual(req_parameters["data.ds_id"], 1)

            self.assertTrue("start_at" in req_parameters)
            self.assertEqual(req_parameters["start_at"], "'2015-07-01'")

            self.assertTrue("variable" not in req_parameters)
            self.assertTrue("intersecting" not in req_parameters)
            self.assertTrue("fields" not in req_parameters)
            self.assertTrue("level" not in req_parameters)

            self.assertEqual(geojson, GeoJSONTest.GEOJSON)

    @patch("requests.get")
    @patch(
        "app.common.client.get_parameters",
        new=Mock(return_value=datasets.convert(PARAMETERS_DEFAULT_TIME_PERIOD)),
    )
    def testWithDefaultTimePeriod(self, get_mock):
        with self.flask_app.app_context():
            get_mock.return_value = setupResponse(
                Response(json.dumps(GeoJSONTest.GEOJSON))
            )

            layer_name = path.make_unique_layer_name(path.VECTOR, 1)
            geojson = client.get_geojson(layer_name)

            req_parameters = self.checkCallArguments(get_mock)

            self.assertTrue("data.ds_id" in req_parameters)
            self.assertEqual(req_parameters["data.ds_id"], 1)

            self.assertTrue("start_at" in req_parameters)
            self.assertEqual(req_parameters["start_at"], "'2015-01-01'")

            self.assertTrue("variable" not in req_parameters)
            self.assertTrue("intersecting" not in req_parameters)
            self.assertTrue("fields" not in req_parameters)
            self.assertTrue("level" not in req_parameters)

            self.assertEqual(geojson, GeoJSONTest.GEOJSON)

    @patch("requests.get")
    @patch(
        "app.common.client.get_parameters",
        new=Mock(return_value=datasets.convert(PARAMETERS_DEFAULT_TIME_PERIOD2)),
    )
    def testWithTimePeriodOverridingDefault(self, get_mock):
        with self.flask_app.app_context():
            get_mock.return_value = setupResponse(
                Response(json.dumps(GeoJSONTest.GEOJSON))
            )

            layer_name = path.make_unique_layer_name(path.VECTOR, 1, time_period="2015")
            geojson = client.get_geojson(layer_name)

            req_parameters = self.checkCallArguments(get_mock)

            self.assertTrue("data.ds_id" in req_parameters)
            self.assertEqual(req_parameters["data.ds_id"], 1)

            self.assertTrue("start_at" in req_parameters)
            self.assertEqual(req_parameters["start_at"], "'2015-01-01'")

            self.assertTrue("variable" not in req_parameters)
            self.assertTrue("intersecting" not in req_parameters)
            self.assertTrue("fields" not in req_parameters)
            self.assertTrue("level" not in req_parameters)

            self.assertEqual(geojson, GeoJSONTest.GEOJSON)

    @patch("requests.get")
    @patch(
        "app.common.client.get_parameters",
        new=Mock(return_value=datasets.convert(PARAMETERS_DEFAULT_FIELDS)),
    )
    def testWithDefaultFields(self, get_mock):
        with self.flask_app.app_context():
            get_mock.return_value = setupResponse(
                Response(json.dumps(GeoJSONTest.GEOJSON))
            )

            layer_name = path.make_unique_layer_name(path.VECTOR, 1)
            geojson = client.get_geojson(layer_name)

            req_parameters = self.checkCallArguments(get_mock)

            self.assertTrue("data.ds_id" in req_parameters)
            self.assertEqual(req_parameters["data.ds_id"], 1)

            self.assertTrue("fields" in req_parameters)
            self.assertEqual(
                req_parameters["fields"],
                GeoJSONTest.PARAMETERS_DEFAULT_FIELDS["default_parameters"]["fields"],
            )

            self.assertTrue("variable" not in req_parameters)
            self.assertTrue("start_at" not in req_parameters)
            self.assertTrue("intersecting" not in req_parameters)
            self.assertTrue("level" not in req_parameters)

            self.assertEqual(geojson, GeoJSONTest.GEOJSON)

    @patch("requests.get")
    @patch(
        "app.common.client.get_parameters",
        new=Mock(return_value=datasets.convert(PARAMETERS_DEFAULT_EMPTY_FIELDS)),
    )
    def testWithDefaultEmptyFields(self, get_mock):
        with self.flask_app.app_context():
            get_mock.return_value = setupResponse(
                Response(json.dumps(GeoJSONTest.GEOJSON))
            )

            layer_name = path.make_unique_layer_name(path.VECTOR, 1)
            geojson = client.get_geojson(layer_name)

            req_parameters = self.checkCallArguments(get_mock)

            self.assertTrue("data.ds_id" in req_parameters)
            self.assertEqual(req_parameters["data.ds_id"], 1)

            self.assertTrue("variable" not in req_parameters)
            self.assertTrue("start_at" not in req_parameters)
            self.assertTrue("intersecting" not in req_parameters)
            self.assertTrue("fields" not in req_parameters)
            self.assertTrue("level" not in req_parameters)

            self.assertEqual(geojson, GeoJSONTest.GEOJSON)

    @patch("requests.get")
    @patch(
        "app.common.client.get_parameters",
        new=Mock(return_value=datasets.convert(PARAMETERS_DEFAULT_LEVEL)),
    )
    def testWithDefaultLevel(self, get_mock):
        with self.flask_app.app_context():
            get_mock.return_value = setupResponse(
                Response(json.dumps(GeoJSONTest.GEOJSON))
            )

            layer_name = path.make_unique_layer_name(path.VECTOR, 1)
            geojson = client.get_geojson(layer_name)

            req_parameters = self.checkCallArguments(get_mock)

            self.assertTrue("data.ds_id" in req_parameters)
            self.assertEqual(req_parameters["data.ds_id"], 1)

            self.assertTrue("level" in req_parameters)
            self.assertEqual(req_parameters["level"], "{country}")

            self.assertTrue("variable" not in req_parameters)
            self.assertTrue("start_at" not in req_parameters)
            self.assertTrue("intersecting" not in req_parameters)
            self.assertTrue("fields" not in req_parameters)

            self.assertEqual(geojson, GeoJSONTest.GEOJSON)

    @patch("requests.get")
    @patch(
        "app.common.client.get_parameters",
        new=Mock(return_value=datasets.convert(PARAMETERS_DEFAULT_INTERSECTING)),
    )
    def testWithDefaultIntersection(self, get_mock):
        with self.flask_app.app_context():
            get_mock.return_value = setupResponse(
                Response(json.dumps(GeoJSONTest.GEOJSON))
            )

            layer_name = path.make_unique_layer_name(path.VECTOR, 1)
            geojson = client.get_geojson(layer_name)

            req_parameters = self.checkCallArguments(get_mock)

            self.assertTrue("data.ds_id" in req_parameters)
            self.assertEqual(req_parameters["data.ds_id"], 1)

            self.assertTrue("intersecting" in req_parameters)
            self.assertEqual(
                req_parameters["intersecting"],
                GeoJSONTest.PARAMETERS_DEFAULT_INTERSECTING["default_parameters"][
                    "intersecting"
                ],
            )

            self.assertTrue("variable" not in req_parameters)
            self.assertTrue("start_at" not in req_parameters)
            self.assertTrue("fields" not in req_parameters)
            self.assertTrue("level" not in req_parameters)

            self.assertEqual(geojson, GeoJSONTest.GEOJSON)

    @patch("requests.get")
    @patch(
        "app.common.client.get_parameters",
        new=Mock(return_value=datasets.convert(PARAMETERS_DEFAULT_INTERSECTING)),
    )
    def testWithIgnoredDefaultIntersection(self, get_mock):
        with self.flask_app.app_context():
            get_mock.return_value = setupResponse(
                Response(json.dumps(GeoJSONTest.GEOJSON))
            )

            layer_name = path.make_unique_layer_name(path.VECTOR, 1)
            geojson = client.get_geojson(layer_name, ignore_intersecting=True)

            req_parameters = self.checkCallArguments(get_mock)

            self.assertTrue("data.ds_id" in req_parameters)
            self.assertEqual(req_parameters["data.ds_id"], 1)

            self.assertTrue("variable" not in req_parameters)
            self.assertTrue("start_at" not in req_parameters)
            self.assertTrue("fields" not in req_parameters)
            self.assertTrue("intersecting" not in req_parameters)
            self.assertTrue("level" not in req_parameters)

            self.assertEqual(geojson, GeoJSONTest.GEOJSON)

    @patch("requests.get")
    @patch(
        "app.common.client.get_parameters",
        new=Mock(return_value=datasets.convert(PARAMETERS)),
    )
    def testIteration(self, get_mock):
        with self.flask_app.app_context():
            response1 = copy.deepcopy(GeoJSONTest.GEOJSON)
            while len(response1["features"]) < 1000:
                response1["features"].append(copy.deepcopy(response1["features"][0]))

            get_mock.return_value = setupResponseWithSideEffect(
                [
                    Response(json.dumps(response1)),
                    Response(json.dumps(GeoJSONTest.GEOJSON)),
                ]
            )

            layer_name = path.make_unique_layer_name(path.VECTOR, 1)
            geojson = client.get_geojson(layer_name)

            self.assertEqual(get_mock.call_count, 2)

            self.assertEqual(len(get_mock.call_args.args), 1)
            self.assertEqual(get_mock.call_args.args[0], "rpc/enermaps_query_geojson")

            self.assertEqual(len(get_mock.call_args.kwargs), 2)

            self.assertTrue("headers" in get_mock.call_args.kwargs)
            self.assertTrue("Authorization" in get_mock.call_args.kwargs["headers"])

            self.assertTrue("params" in get_mock.call_args.kwargs)
            self.assertTrue("parameters" in get_mock.call_args.kwargs["params"])
            self.assertTrue("row_offset" in get_mock.call_args.kwargs["params"])
            self.assertTrue("row_limit" in get_mock.call_args.kwargs["params"])
            self.assertEqual(get_mock.call_args.kwargs["params"]["row_offset"], 1000)
            self.assertEqual(get_mock.call_args.kwargs["params"]["row_limit"], 1000)

            req_parameters = json.loads(
                get_mock.call_args.kwargs["params"]["parameters"]
            )

            self.assertTrue("data.ds_id" in req_parameters)
            self.assertEqual(req_parameters["data.ds_id"], 1)

            self.assertTrue("variable" not in req_parameters)
            self.assertTrue("start_at" not in req_parameters)
            self.assertTrue("intersecting" not in req_parameters)
            self.assertTrue("fields" not in req_parameters)
            self.assertTrue("level" not in req_parameters)

            self.assertEqual(len(geojson["features"]), 1001)

    @patch("requests.get")
    @patch(
        "app.common.client.get_parameters",
        new=Mock(return_value=datasets.convert(PARAMETERS)),
    )
    def testFailure(self, get_mock):
        with self.flask_app.app_context():
            get_mock.side_effect = Exception()

            layer_name = path.make_unique_layer_name(path.VECTOR, 1)
            geojson = client.get_geojson(layer_name, ignore_intersecting=True)

            self.assertTrue(geojson is None)


class AeraTest(BaseApiTest):

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
        ],
    }

    @patch("requests.get")
    def testSuccess(self, get_mock):
        with self.flask_app.app_context():
            get_mock.return_value = setupResponse(
                Response(json.dumps(AeraTest.GEOJSON))
            )

            geojson = client.get_area("NUTS1")

            self.assertEqual(get_mock.call_count, 1)

            self.assertEqual(len(get_mock.call_args.args), 1)
            self.assertEqual(get_mock.call_args.args[0], "rpc/enermaps_query_geojson")

            self.assertEqual(len(get_mock.call_args.kwargs), 2)

            self.assertTrue("headers" in get_mock.call_args.kwargs)
            self.assertTrue("Authorization" in get_mock.call_args.kwargs["headers"])

            self.assertTrue("params" in get_mock.call_args.kwargs)
            self.assertTrue("parameters" in get_mock.call_args.kwargs["params"])
            self.assertTrue("row_offset" in get_mock.call_args.kwargs["params"])
            self.assertTrue("row_limit" in get_mock.call_args.kwargs["params"])
            self.assertEqual(get_mock.call_args.kwargs["params"]["row_offset"], 0)
            self.assertEqual(get_mock.call_args.kwargs["params"]["row_limit"], 1000)

            req_parameters = json.loads(
                get_mock.call_args.kwargs["params"]["parameters"]
            )

            self.assertTrue("data.ds_id" in req_parameters)
            self.assertEqual(req_parameters["data.ds_id"], 0)

            self.assertTrue("level" in req_parameters)
            self.assertEqual(req_parameters["level"], "{NUTS1}")

            self.assertTrue("variable" not in req_parameters)
            self.assertTrue("start_at" not in req_parameters)
            self.assertTrue("intersecting" not in req_parameters)
            self.assertTrue("fields" not in req_parameters)

            self.assertEqual(geojson, AeraTest.GEOJSON)

    @patch("requests.get")
    def testFailure(self, get_mock):
        with self.flask_app.app_context():
            get_mock.side_effect = Exception()

            geojson = client.get_area("NUTS1")
            self.assertTrue(geojson is None)


class LegendTest(BaseApiTest):

    LEGEND = {"symbology": []}
    LEGEND2 = {"symbology": ["2"]}

    PARAMETERS_DEFAULT_INTERSECTING = {
        "end_at": None,
        "parameters": {
            "end_at": None,
            "fields": [],
            "levels": [],
            "is_tiled": False,
            "start_at": None,
            "is_raster": False,
            "variables": [],
            "time_periods": [],
            "temporal_granularity": None,
        },
        "default_parameters": {
            "intersecting": (
                "POLYGON((2.29 48.88,2.29 48.87,2.3 48.87,2.3 48.88,2.29 48.88))"
            )
        },
    }

    @patch("requests.get")
    @patch(
        "app.common.client.get_parameters",
        new=Mock(return_value=datasets.convert(PARAMETERS_DEFAULT_INTERSECTING)),
    )
    def testSuccess(self, get_mock):
        with self.flask_app.app_context():
            get_mock.return_value = setupResponse(
                Response(json.dumps(LegendTest.LEGEND))
            )

            layer_name = path.make_unique_layer_name(path.VECTOR, 1)
            legend = client.get_legend(layer_name, ttl_hash=100)

            self.assertEqual(get_mock.call_count, 1)

            self.assertEqual(len(get_mock.call_args.args), 1)
            self.assertEqual(get_mock.call_args.args[0], "rpc/enermaps_get_legend")

            self.assertEqual(len(get_mock.call_args.kwargs), 2)

            self.assertTrue("headers" in get_mock.call_args.kwargs)
            self.assertTrue("Authorization" in get_mock.call_args.kwargs["headers"])

            self.assertTrue("params" in get_mock.call_args.kwargs)
            self.assertTrue("parameters" in get_mock.call_args.kwargs["params"])

            req_parameters = json.loads(
                get_mock.call_args.kwargs["params"]["parameters"]
            )

            self.assertTrue("data.ds_id" in req_parameters)
            self.assertEqual(req_parameters["data.ds_id"], 1)

            self.assertTrue("variable" not in req_parameters)
            self.assertTrue("start_at" not in req_parameters)
            self.assertTrue("level" not in req_parameters)
            self.assertTrue("intersecting" not in req_parameters)
            self.assertTrue("fields" not in req_parameters)

            self.assertEqual(legend, LegendTest.LEGEND)

    @patch("requests.get")
    @patch(
        "app.common.client.get_parameters",
        new=Mock(return_value=datasets.convert(PARAMETERS_DEFAULT_INTERSECTING)),
    )
    def testCaching(self, get_mock):
        with self.flask_app.app_context():
            get_mock.return_value = setupResponse(
                Response(json.dumps(LegendTest.LEGEND))
            )

            layer_name = path.make_unique_layer_name(path.VECTOR, 1)

            legend1 = client.get_legend(layer_name, ttl_hash=200)

            get_mock.return_value = setupResponse(
                Response(json.dumps(LegendTest.LEGEND2))
            )

            legend2 = client.get_legend(layer_name, ttl_hash=200)

            self.assertEqual(get_mock.call_count, 1)
            self.assertEqual(legend1, legend2)
            self.assertEqual(legend1, LegendTest.LEGEND)

            legend3 = client.get_legend(layer_name, ttl_hash=300)

            self.assertEqual(get_mock.call_count, 2)
            self.assertEqual(legend3, LegendTest.LEGEND2)

    @patch("requests.get")
    @patch(
        "app.common.client.get_parameters",
        new=Mock(return_value=datasets.convert(PARAMETERS_DEFAULT_INTERSECTING)),
    )
    def testFailure(self, get_mock):
        with self.flask_app.app_context():
            get_mock.side_effect = Exception()

            layer_name = path.make_unique_layer_name(path.VECTOR, 1)
            legend = client.get_legend(layer_name, ttl_hash=900)
            self.assertTrue(legend is None)
