import requests

from app.common.test import BaseApiTest, BaseIntegrationTest


class FakeOuputTest(BaseIntegrationTest):
    def testCalculationModuleWorkflow(self):
        """Test for the following workflow:
        * get the list of calculation module
        * call the expected default cm (multiply)
        * check the result
        """
        requests.get(self.url)

    def testCalculationModuleBrokenParameter(self):
        """Test for the following workflow:
        * get the list of calculation module
        * call the expected default cm (multiply)
        * check the result
        """
