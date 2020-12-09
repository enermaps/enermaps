"""Test for the calculation modules
"""
import json

import requests

import app.common.filepath as filepath
from app.common.test import BaseIntegrationTest


class FakeOuputTest(BaseIntegrationTest):
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
        with open(filepath.get_testdata_path("example.geojson"), "rb") as fd:
            selection = json.load(fd)
        cm_task_parameters = {}

        cm_task_parameters["selection"] = selection
        cm_task_parameters["parameters"] = {"factor": 1}
        cm_task_parameters["layers"] = ["gfa_tot_curr_density.tiff"]
        create_task_url = self.cm_url + "/" + first_cm_name + "/task"
        resp = requests.post(create_task_url, json=cm_task_parameters)
        dict_resp = self.getJSONFromRequestResponse(resp)
        self.assertGreater(
            len(dict_resp), 0, msg="Answer from creating a task" " was " + resp.text
        )
        # TODO here the format of the answer is still a work in progress,
        # so we don't check anything yet.

    def testCalculationModuleBrokenParameter(self):
        """Test for the a non existant calculation module"""
        resp = requests.post(self.cm_url + "/" + "nonexistantcm" + "/task")
        self.assertFalse(resp.ok)
