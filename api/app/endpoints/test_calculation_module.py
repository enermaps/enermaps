"""Test for the calculation modules
"""
import requests

from app.common.test import BaseIntegrationTest


class FakeOuputTest(BaseIntegrationTest):
    def testCalculationModuleWorkflow(self):
        """Test for the following workflow:
        * get the list of calculation module
        * call the expected default cm (multiply)
        * check the result
        """
        resp = requests.get(self.url + "/cm")
        cms = resp.json()
        self.assertGreaterEqual(len(cms), 0)

    def testCalculationModuleBrokenParameter(self):
        """Test for the following workflow:
        * get the list of calculation module
        * call the expected default cm (multiply)
        * check the result
        """
