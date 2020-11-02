import io

from app.common.test import BaseApiTest
from lxml import etree
from PIL import Image

import app.common.xml as xml

GETCAPABILITIES_ARGS = {"service": "WMS", "request": "GetCapabilities"}


class BaseWMSTEst(BaseApiTest):
    def testFailWhenNoService(self):
        response = self.client.get("api/wms", query_string={"request": "GetMap"})
        self.assertEqual(response.status, "400 BAD REQUEST", response.data)

    def testFailWhenNoRequest(self):
        response = self.client.get("api/wms", query_string={"service": "WMS"})
        self.assertEqual(response.status, "404 NOT FOUND", response.data)


class WMSGetCapabilitiesTest(BaseApiTest):
    """Test the get capabilities (a list of all endpoint and layer)"""

    def testLayerLessCall(self):
        """Test the call to getCapabilities"""
        # help(self.client.get)
        response = self.client.get("api/wms", query_string=GETCAPABILITIES_ARGS)
        self.assertEqual(response.status, "200 OK", response.data)
        root = xml.etree_fromstring(response.data)
        layer_names = root.findall(".//Layer/Name")
        self.assertEqual(len(layer_names), 0)

    def _testLayerList(self, testfile, is_queryable):
        """Upon adding a layer, we should see that layer
        in the capability layer list"""
        test_data, testfile_content = self.get_testformdata(testfile)
        response = self.client.post(
            "api/geofile/", data=test_data, content_type="multipart/form-data"
        )
        self.assertEqual(response.status, "200 OK", response.data)
        response.close()

        response = self.client.get("api/wms", query_string=GETCAPABILITIES_ARGS)
        self.assertEqual(response.status, "200 OK", response.data)
        root = etree.fromstring(response.data)
        layers = root.findall(".//Layer/Layer")
        self.assertEqual(len(layers), 1)
        layer = layers[0]
        self.assertEqual(layer.get("queryable"), is_queryable)

        self.assertEqual(layer.find("Name").text, testfile)

    def testVectorLayerList(self):
        self._testLayerList("nuts.zip", is_queryable="1")

    def testRasterLayerList(self):
        testfile = "hotmaps-cdd_curr_adapted.tif"
        self._testLayerList(testfile, is_queryable="0")


class WMSGetMapTest(BaseApiTest):
    """Test the wms GetMap endpoint"""

    TILE_PARAMETERS = {
        "service": "WMS",
        "request": "GetMap",
        "layers": "",
        "styles": "",
        "format": "image/png",
        "transparent": "true",
        "version": "1.1.1",
        "width": "256",
        "height": "256",
        "srs": "EPSG:3857",
        "bbox": "19567.87924100512,6809621.975869781,"
        "39135.75848201024,6829189.85511079",
    }

    GETMAP_ARGS = {"service": "WMS", "request": "GetMap"}

    def testVectorTileWorkflow(self):
        testfile = "nuts.zip"
        test_data, testfile_content = self.get_testformdata(testfile)
        response = self.client.post(
            "api/geofile/", data=test_data, content_type="multipart/form-data"
        )
        self.assertEqual(response.status, "200 OK", response.data)
        response.close()
        args = self.TILE_PARAMETERS
        args["layers"] = testfile
        response = self.client.get("api/wms", query_string=self.TILE_PARAMETERS)
        self.assertEqual(response.status, "200 OK")
        self.assertGreater(len(response.data), 0)
        Image.open(io.BytesIO(response.data))

    def testRasterTileWorkflow(self):
        """Upload a raster, then check that the tile request is not empty"""
        testfile = "hotmaps-cdd_curr_adapted.tif"
        test_data, testfile_content = self.get_testformdata(testfile)
        response = self.client.post(
            "api/geofile/", data=test_data, content_type="multipart/form-data"
        )
        self.assertEqual(response.status, "200 OK", response.data)
        response.close()

        args = self.TILE_PARAMETERS
        args["layers"] = testfile
        response = self.client.get("api/wms", query_string=self.TILE_PARAMETERS)
        self.assertEqual(response.status, "200 OK")
        self.assertGreater(len(response.data), 0)
        Image.open(io.BytesIO(response.data))
        # test that we received an image
