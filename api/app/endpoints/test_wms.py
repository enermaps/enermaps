from lxml import etree

from app.common.test import BaseApiTest


class BaseWMSTEst(BaseApiTest):
    def testFailWhenNoService(self):
        response = self.client.get("api/wms", query_string={"request": "GetMap"})
        self.assertEqual(response.status, "400 BAD REQUEST", response.data)

    def testFailWhenNoRequest(self):
        response = self.client.get("api/wms", query_string={"service": "WMS"})
        self.assertEqual(response.status, "404 NOT FOUND", response.data)


class WMSGetCapabilitiesTest(BaseApiTest):
    """Test the get capabilities (a list of all endpoint and layer)"""

    BASE_ARGS = {"service": "WMS", "request": "GetCapabilities"}

    def testLayerLessCall(self):
        """Test the call to getCapabilities"""
        args = self.BASE_ARGS

        # help(self.client.get)
        response = self.client.get("api/wms", query_string=args)
        self.assertEqual(response.status, "200 OK", response.data)
        etree.fromstring(response.data)
