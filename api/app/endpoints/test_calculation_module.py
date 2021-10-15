"""Test for the calculation modules
"""
import json
import os
import shutil
from unittest.mock import Mock, patch
from urllib.parse import urlparse

import requests

from app.common import path
from app.common.test import BaseApiTest, BaseIntegrationTest
from app.models import storage


class MockCM:
    def __init__(self, status="PENDING", result=None):
        self.name = "mock_cm"
        self.pretty_name = "Mock CM"
        self.parameters = ["selection", "rasters", "params"]
        self.schema = {}
        self.called_with_args = []
        self.status = status
        self.result = result

    def call(self, *args):
        self.called_with_args = args
        return "01234567-0000-0000-0000-000000000000"

    def ready(self):
        return not (self.status in ("PENDING", "REVOKED"))

    def get(self, timeout=0):
        if self.result is not None:
            return self.result

        raise Exception("Some problem")

    def revoke(self, terminate=True):
        self.status = "REVOKED"


class CMListTest(BaseApiTest):

    CM_LIST = {"mock_cm": MockCM()}

    @patch(
        "app.models.calculation_module.list_cms",
        new=Mock(return_value=CM_LIST),
    )
    def testGetCMs(self):
        response = self.client.get("api/cm/")
        self.assertEqual(response.status_code, 200)

        data = response.json
        self.assertEqual(len(data), len(CMListTest.CM_LIST))

        for name, ref in CMListTest.CM_LIST.items():
            cms = [x for x in data if x["name"] == name]
            self.assertEqual(len(cms), 1)

            cm = cms[0]
            self.assertEqual(len(cm), 4)

            self.assertEqual(cm["name"], ref.name)
            self.assertEqual(cm["pretty_name"], ref.pretty_name)
            self.assertEqual(cm["parameters"], ref.parameters)
            self.assertEqual(cm["schema"], ref.schema)

    def testPostNotAllowed(self):
        response = self.client.post("api/cm/")
        self.assertEqual(response.status_code, 405)

    def testPutNotAllowed(self):
        response = self.client.put("api/cm/")
        self.assertEqual(response.status_code, 405)

    def testDeleteNotAllowed(self):
        response = self.client.delete("api/cm/")
        self.assertEqual(response.status_code, 405)


class CMTaskCreatorTest(BaseApiTest):

    CM = MockCM()

    def setUp(self):
        super().setUp()

        with self.flask_app.app_context():
            # Copy the raster dataset
            layer_name = path.make_unique_layer_name(path.RASTER, 42)
            storage_instance = storage.create(layer_name)

            os.makedirs(storage_instance.get_dir(layer_name))

            shutil.copy(
                self.get_testdata_path("hotmaps-cdd_curr_adapted.tif"),
                storage_instance.get_file_path(layer_name, "FID1.tif"),
            )

            shutil.copy(
                self.get_testdata_path("hotmaps-cdd_curr_adapted.tif"),
                storage_instance.get_file_path(layer_name, "FID2.tif"),
            )

    @patch(
        "app.models.calculation_module.cm_by_name",
        new=Mock(return_value=CM),
    )
    def testCreateTask(self):
        parameters = {
            "selection": {"area1": 10},
            "layer": "raster/42",
            "parameters": {"param1": 4},
        }

        response = self.client.post("api/cm/mock_cm/task/", json=parameters)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            urlparse(response.location).path,
            "/api/cm/mock_cm/task/01234567-0000-0000-0000-000000000000/",
        )

        args = CMTaskCreatorTest.CM.called_with_args
        self.assertEqual(len(args), 3)
        self.assertEqual(args[0], parameters["selection"])
        self.assertEqual(args[1], ["42/FID1.tif", "42/FID2.tif"])
        self.assertEqual(args[2], parameters["parameters"])

    def testGetNotAllowed(self):
        response = self.client.get("api/cm/mock_cm/task/")
        self.assertEqual(response.status_code, 405)

    def testPutNotAllowed(self):
        response = self.client.put("api/cm/mock_cm/task/")
        self.assertEqual(response.status_code, 405)

    def testDeleteNotAllowed(self):
        response = self.client.delete("api/cm/mock_cm/task/")
        self.assertEqual(response.status_code, 405)


class CMTaskTest(BaseApiTest):
    @patch(
        "app.models.calculation_module.task_by_id",
        new=Mock(return_value=MockCM()),
    )
    def testGetPendingTask(self):
        response = self.client.get(
            "api/cm/mock_cm/task/01234567-0000-0000-0000-000000000000/"
        )
        self.assertEqual(response.status_code, 200)

        data = response.json

        self.assertEqual(data["cm_name"], "mock_cm")
        self.assertEqual(data["task_id"], "01234567-0000-0000-0000-000000000000")
        self.assertEqual(data["status"], "PENDING")
        self.assertEqual(data["result"], "")

    @patch(
        "app.models.calculation_module.task_by_id",
        new=Mock(
            return_value=MockCM(status="SUCCESS", result={"value1": 10, "value2": 20})
        ),
    )
    def testGetSuccessfulTask(self):
        response = self.client.get(
            "api/cm/mock_cm/task/01234567-0000-0000-0000-000000000000/"
        )
        self.assertEqual(response.status_code, 200)

        data = response.json

        self.assertEqual(data["cm_name"], "mock_cm")
        self.assertEqual(data["task_id"], "01234567-0000-0000-0000-000000000000")
        self.assertEqual(data["status"], "SUCCESS")
        self.assertEqual(data["result"], {"value1": 10, "value2": 20})

    @patch(
        "app.models.calculation_module.task_by_id",
        new=Mock(return_value=MockCM(status="FAILURE")),
    )
    def testGetFailedTask(self):
        response = self.client.get(
            "api/cm/mock_cm/task/01234567-0000-0000-0000-000000000000/"
        )
        self.assertEqual(response.status_code, 200)

        data = response.json

        self.assertEqual(data["cm_name"], "mock_cm")
        self.assertEqual(data["task_id"], "01234567-0000-0000-0000-000000000000")
        self.assertEqual(data["status"], "FAILURE")
        self.assertEqual(data["result"], "Some problem")

    @patch(
        "app.models.calculation_module.task_by_id",
        new=Mock(return_value=MockCM(status="REVOKED")),
    )
    def testGetRevokedTask(self):
        response = self.client.get(
            "api/cm/mock_cm/task/01234567-0000-0000-0000-000000000000/"
        )
        self.assertEqual(response.status_code, 200)

        data = response.json

        self.assertEqual(data["cm_name"], "mock_cm")
        self.assertEqual(data["task_id"], "01234567-0000-0000-0000-000000000000")
        self.assertEqual(data["status"], "REVOKED")
        self.assertEqual(data["result"], "")

    @patch(
        "app.models.calculation_module.task_by_id",
        new=Mock(return_value=MockCM(status="SUCCESS")),
    )
    def testGetTaskUnexpectedError(self):
        response = self.client.get(
            "api/cm/mock_cm/task/01234567-0000-0000-0000-000000000000/"
        )
        self.assertEqual(response.status_code, 200)

        data = response.json

        self.assertEqual(data["cm_name"], "mock_cm")
        self.assertEqual(data["task_id"], "01234567-0000-0000-0000-000000000000")
        self.assertEqual(data["status"], "FAILURE")
        self.assertEqual(data["result"], "An unexpected error happened: Some problem")

    @patch(
        "app.models.calculation_module.task_by_id",
        new=Mock(return_value=MockCM()),
    )
    def testRevokeTask(self):
        response = self.client.delete(
            "api/cm/mock_cm/task/01234567-0000-0000-0000-000000000000/"
        )
        self.assertEqual(response.status_code, 200)

        data = response.json

        self.assertEqual(data["cm_name"], "mock_cm")
        self.assertEqual(data["task_id"], "01234567-0000-0000-0000-000000000000")
        self.assertEqual(data["status"], "REVOKED")

    def testPostNotAllowed(self):
        response = self.client.post(
            "api/cm/mock_cm/task/01234567-0000-0000-0000-000000000000/"
        )
        self.assertEqual(response.status_code, 405)

    def testPutNotAllowed(self):
        response = self.client.put(
            "api/cm/mock_cm/task/01234567-0000-0000-0000-000000000000/"
        )
        self.assertEqual(response.status_code, 405)


class CMTaskGeoJSONTest(BaseApiTest):
    def testUploadTIFF(self):
        tiff_file = "hotmaps-cdd_curr_adapted.tif"
        files, _ = self.prepare_file_upload(tiff_file)

        response = self.client.post(
            "api/cm/mock_cm/task/01234567-0000-0000-0000-000000000000/geofile/",
            data=files,
            content_type="multipart/form-data",
        )
        self.assertStatusCodeEqual(response, 201)

        final_path = os.path.join(
            self.cm_outputs_dir,
            "mock_cm/01/23/45/67/01234567-0000-0000-0000-000000000000",
            tiff_file,
        )
        self.assertTrue(os.path.exists(final_path))

    def testUploadTIFFWithTwoFs(self):
        tiff_file = "hotmaps-cdd_curr_adapted.tif"
        files, _ = self.prepare_file_upload(
            tiff_file, dest_filename="hotmaps-cdd_curr_adapted.tiff"
        )

        response = self.client.post(
            "api/cm/mock_cm/task/01234567-0000-0000-0000-000000000000/geofile/",
            data=files,
            content_type="multipart/form-data",
        )
        self.assertStatusCodeEqual(response, 201)

        final_path = os.path.join(
            self.cm_outputs_dir,
            "mock_cm/01/23/45/67/01234567-0000-0000-0000-000000000000",
            tiff_file,
        )
        self.assertTrue(os.path.exists(final_path))

    def testUploadTIFFWithUnicode(self):
        tiff_file = "hotmaps-cdd_curr_adapted.tif"
        files, _ = self.prepare_file_upload(tiff_file, dest_filename="hotmaps⎈.tif")

        response = self.client.post(
            "api/cm/mock_cm/task/01234567-0000-0000-0000-000000000000/geofile/",
            data=files,
            content_type="multipart/form-data",
        )
        self.assertStatusCodeEqual(response, 201)

        final_path = os.path.join(
            self.cm_outputs_dir,
            "mock_cm/01/23/45/67/01234567-0000-0000-0000-000000000000",
            "hotmaps.tif",
        )
        self.assertTrue(os.path.exists(final_path))

    def testUploadTIFFWithFolder(self):
        tiff_file = "hotmaps-cdd_curr_adapted.tif"
        files, _ = self.prepare_file_upload(
            tiff_file, dest_filename="subfolder/hotmaps.tif"
        )

        response = self.client.post(
            "api/cm/mock_cm/task/01234567-0000-0000-0000-000000000000/geofile/",
            data=files,
            content_type="multipart/form-data",
        )
        self.assertStatusCodeEqual(response, 201)

        final_path = os.path.join(
            self.cm_outputs_dir,
            "mock_cm/01/23/45/67/01234567-0000-0000-0000-000000000000",
            "subfolderhotmaps.tif",
        )
        self.assertTrue(os.path.exists(final_path))

    def testUploadTIFFWithUpperFolder(self):
        tiff_file = "hotmaps-cdd_curr_adapted.tif"
        files, _ = self.prepare_file_upload(tiff_file, dest_filename="../hotmaps.tif")

        response = self.client.post(
            "api/cm/mock_cm/task/01234567-0000-0000-0000-000000000000/geofile/",
            data=files,
            content_type="multipart/form-data",
        )
        self.assertStatusCodeEqual(response, 201)

        final_path = os.path.join(
            self.cm_outputs_dir,
            "mock_cm/01/23/45/67/01234567-0000-0000-0000-000000000000",
            "hotmaps.tif",
        )
        self.assertTrue(os.path.exists(final_path))

    def testUploadTIFFWithHiddenFileName(self):
        tiff_file = "hotmaps-cdd_curr_adapted.tif"
        files, _ = self.prepare_file_upload(tiff_file, dest_filename=".hotmaps.tif")

        response = self.client.post(
            "api/cm/mock_cm/task/01234567-0000-0000-0000-000000000000/geofile/",
            data=files,
            content_type="multipart/form-data",
        )
        self.assertStatusCodeEqual(response, 201)

        final_path = os.path.join(
            self.cm_outputs_dir,
            "mock_cm/01/23/45/67/01234567-0000-0000-0000-000000000000",
            "hotmaps.tif",
        )
        self.assertTrue(os.path.exists(final_path))

    def testUploadTIFFWithoutProjection(self):
        tiff_file = "no_projection.tif"
        files, _ = self.prepare_file_upload(tiff_file)

        response = self.client.post(
            "api/cm/mock_cm/task/01234567-0000-0000-0000-000000000000/geofile/",
            data=files,
            content_type="multipart/form-data",
        )
        self.assertStatusCodeEqual(response, 400)

        final_path = os.path.join(
            self.cm_outputs_dir,
            "mock_cm/01/23/45/67/01234567-0000-0000-0000-000000000000",
            "no_projection.tif",
        )
        self.assertFalse(os.path.exists(final_path))

    def testGetNotAllowed(self):
        response = self.client.get(
            "api/cm/mock_cm/task/01234567-0000-0000-0000-000000000000/geofile/"
        )
        self.assertEqual(response.status_code, 405)

    def testPutNotAllowed(self):
        response = self.client.put(
            "api/cm/mock_cm/task/01234567-0000-0000-0000-000000000000/geofile/"
        )
        self.assertEqual(response.status_code, 405)

    def testDeleteNotAllowed(self):
        response = self.client.delete(
            "api/cm/mock_cm/task/01234567-0000-0000-0000-000000000000/geofile/"
        )
        self.assertEqual(response.status_code, 405)


class FakeOutputTest(BaseIntegrationTest):
    def setUp(self):
        super().setUp()
        self.cm_url = self.api_url + "/cm"

    def getJSONFromRequestResponse(self, resp):
        """Assert that a requests answer is a json
        throw a jsonDecodeError if not with the content
        of the answer.
        """
        self.assertTrue(resp.ok, msg="")
        try:
            dict_resp = resp.json()
        except json.JSONDecodeError as err:
            err.msg += ", content received was " + resp.text
            raise err
        return dict_resp

    def _getFirstCMName(self):
        """Return first CM name."""
        resp = requests.get(self.cm_url)
        dict_resp = self.getJSONFromRequestResponse(resp)
        self.assertIn("cms", dict_resp)
        cms = dict_resp["cms"]
        self.assertGreaterEqual(len(cms), 0)
        first_cm = cms[0]
        self.assertIn("name", first_cm)
        return first_cm["name"]

    def testCalculationModuleWorkflow(self):
        """Test for the following workflow:
        * get the list of calculation module
        * call the expected default cm (multiply)
        * check that we created the task successfully
        """
        first_cm_name = self._getFirstCMName()

        # Call the calculation module with a simplified
        # bounding box, a rectangle around switzerland
        with open(self.get_testdata_path("example.geojson"), "rb") as fd:
            selection = json.load(fd)
        cm_task_parameters = {}

        cm_task_parameters["selection"] = selection
        cm_task_parameters["parameters"] = {"factor": 1}
        cm_task_parameters["layers"] = ["gfa_tot_curr_density.tiff"]
        create_task_url = self.cm_url + "/" + first_cm_name + "/task"
        self.url = create_task_url
        resp = requests.post(self.url, json=cm_task_parameters)
        dict_resp = self.getJSONFromRequestResponse(resp)
        self.assertGreater(
            len(dict_resp), 0, msg="Answer from creating a task" " was " + resp.text
        )
        # TODO here the format of the answer is still a work in progress,
        # so we don't check anything yet.

    def testCalculationModuleBrokenParameter(self):
        """Test for the a non existant calculation module"""
        resp = requests.post(self.cm_url + "/" + "nonexistantcm" + "/task")
        self.assertEqual(resp.status_code, 404)
