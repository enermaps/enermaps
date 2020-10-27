import json

from app.common.test import BaseApiTest


class FakeOuputTest(BaseApiTest):
    def testFormatFakeOutput(self):
        """Check that the result is ok and in JSON format"""
        response = self.client.get("api/cm/0/task/0")
        self.assertEqual(response.status, "200 OK", response.data)

        json_content = json.loads(response.data)
