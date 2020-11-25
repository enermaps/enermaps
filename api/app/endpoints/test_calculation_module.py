import requests

from app.common.test import BaseApiTest, labeledTest


@labeledTest("integration")
class FakeOuputTest(BaseApiTest):
    def testCalculationModuleWorkflow(self):
        """Test for the following workflow:
        * get the list of calculation module
        * call the expected default cm (multiply)
        * check the result
        """
        requests.get("http://127.0.0.1:8000", )


    def testCalculationModuleBrokenParameter(self):
        """Test for the following workflow:
        * get the list of calculation module
        * call the expected default cm (multiply)
        * check the result
        """
