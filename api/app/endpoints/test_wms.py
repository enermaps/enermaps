import io
import json

import lxml
from lxml import etree
from owslib.wms import WebMapService
from PIL import Image

import app.common.xml as xml
from app.common import filepath
from app.common.test import BaseApiTest, BaseIntegrationTest

GETCAPABILITIES_ARGS = {"service": "WMS", "request": "GetCapabilities"}


class BaseWMSTest(BaseApiTest):
    def testFailWhenNoRequestSpecified(self):
        """Try to achieve the WMS without request."""
        response = self.client.get("api/wms", query_string={"service": "WMS"})
        self.assertEqual(response.status, "400 BAD REQUEST", response.data)


class WMSGetCapabilitiesTest(BaseApiTest):
    """Test the get capabilities (a list of all endpoint and layer)"""

    @classmethod
    def setUpClass(cl):
        """Create the xml schema validator."""
        schema_path = filepath.get_testdata_path("WMS_MS_Capabilities_1.3.0.xsd")
        # load additonal schemas
        with open(schema_path, "rb") as schema_fd:
            xmlschema = xml.etree_fromstring(schema_fd.read())

        schema_path = filepath.get_testdata_path("xml.xsd")
        newimport = lxml.etree.Element(
            "{http://www.w3.org/2001/XMLSchema}import",
            namespace="http://www.w3.org/2001/xml.xsd",
            schemaLocation="file://" + schema_path,
        )
        xmlschema.insert(0, newimport)

        schema_path = filepath.get_testdata_path("xlink.xsd")
        newimport = lxml.etree.Element(
            "{http://www.w3.org/2001/XMLSchema}import",
            namespace="http://www.w3.org/1999/xlink.xsd",
            schemaLocation="file://" + schema_path,
        )
        xmlschema.insert(1, newimport)
        cl.schema = etree.XMLSchema(xmlschema)

    def testSucceedWithUppercaseParameters(self):
        """Test that lowercase parameters produces the same result as uppercase
        get parameters
        """
        args = {}
        for k, v in GETCAPABILITIES_ARGS.items():
            args[k.upper()] = v
        response_lower = self.client.get("api/wms", query_string=args)
        response_upper = self.client.get("api/wms", query_string=GETCAPABILITIES_ARGS)
        self.assertEqual(response_lower.data, response_upper.data)
        self._validate_xml_string(response_lower.data)

    def testFailsWhenNoService(self):
        """Test that the call to getcapabilities fails when no service
        parameter is passed as argument
        """
        args = GETCAPABILITIES_ARGS
        del args["service"]
        response = self.client.get("api/wms", query_string={"request": args})
        self.assertEqual(response.status, "400 BAD REQUEST", response.data)

    def testLayerLessCall(self):
        """Test that the call to getCapabilities with no layers defined
        returns an empty list of layers.
        """
        # help(self.client.get)
        response = self.client.get("api/wms", query_string=GETCAPABILITIES_ARGS)
        self.assertStatusCodeEqual(response, 200)
        root = xml.etree_fromstring(response.data)
        layer_names = root.findall(".//Layer/Layer/Name", root.nsmap)
        self.assertEqual(len(layer_names), 0, "Found a layer, expected none")
        self._validate_xml(root)

    def _testLayerList(self, testfile, is_queryable):
        """Upon adding a layer, we should see that layer
        in the capability layer list"""
        test_data, testfile_content = self.get_testformdata(testfile)
        response = self.client.post(
            "api/geofile/",
            data=test_data,
            content_type="multipart/form-data",
            follow_redirects=True,
        )
        self.assertStatusCodeEqual(response, 200)

        response = self.client.get("api/wms", query_string=GETCAPABILITIES_ARGS)
        self.assertStatusCodeEqual(response, 200)
        root = etree.fromstring(response.data)
        layers = root.findall(".//Layer/Layer", root.nsmap)
        self.assertEqual(len(layers), 1)
        layer = layers[0]
        self.assertEqual(layer.get("queryable", root.nsmap), is_queryable)
        self.assertEqual(layer.find("Name", root.nsmap).text, testfile)
        # finally test the response compatiblity using the dtd, a xml schema
        self._validate_xml(root)

    def testVectorLayerList(self):
        """Verify that upon uploading a non-raster layer, we return a
        list of layers containing the uploaded non-raster layer with
        the queryable attribute.
        This means that this layer supports the getfeatureinfo endpoint.
        """
        self._testLayerList("nuts.zip", is_queryable="1")

    def testRasterLayerList(self):
        """Verify that upon uploading a raster layer, we return a
        list of layers containing the uploaded raster layer.
        """
        testfile = "hotmaps-cdd_curr_adapted.tif"
        self._testLayerList(testfile, is_queryable="0")

    def _validate_xml_string(self, xml_string):
        """Validate a xml schema saved as string based on the xml validator."""
        root = etree.fromstring(xml_string)
        self._validate_xml(root)

    def _validate_xml(self, xml_root):
        """Validate a xml schema based on the xml validator."""
        valid = self.schema.validate(xml_root)
        self.assertTrue(valid, self.schema.error_log.filter_from_errors())


class WMSGetMapTest(BaseApiTest):
    """Test the wms GetMap endpoint"""

    TILE_SIZE = (256, 256)
    TILE_PARAMETERS = {
        "service": "WMS",
        "request": "GetMap",
        "layers": "",
        "styles": "",
        "format": "image/png",
        "transparent": "true",
        "version": "1.1.1",
        "width": str(TILE_SIZE[0]),
        "height": str(TILE_SIZE[1]),
        "srs": "EPSG:3857",
        "bbox": "19567.87924100512,6809621.975869781"
        ","
        "39135.75848201024,6829189.85511079",
    }

    GETMAP_ARGS = {"service": "WMS", "request": "GetMap"}

    def testVectorTileWorkflow(self):
        """Post a vector file, retrieve it as image from WMS endpoint,
        check if the image has the right size  without being empty.
        """
        testfile = "nuts.zip"
        test_data, testfile_content = self.get_testformdata(testfile)
        response = self.client.post(
            "api/geofile/",
            data=test_data,
            content_type="multipart/form-data",
            follow_redirects=True,
        )
        self.assertStatusCodeEqual(response, 200)
        response.close()
        args = self.TILE_PARAMETERS
        args["layers"] = testfile
        response = self.client.get("api/wms", query_string=self.TILE_PARAMETERS)
        self.assertStatusCodeEqual(response, 200)
        self.assertGreater(len(response.data), 0)
        image = Image.open(io.BytesIO(response.data))
        self.assertEqual(image.size, self.TILE_SIZE)
        self.assertEqual(image.size, self.TILE_SIZE)
        self.assertEqual(image.format, "PNG")
        empty_pixel = 0
        for x in range(image.width):
            for y in range(image.height):
                pixel = image.getpixel((x, y))
                if pixel == (0, 0, 0, 0):
                    empty_pixel += 1
        total_pixel = image.width * image.height
        non_empty_pixel = total_pixel - empty_pixel
        self.assertNotEqual(non_empty_pixel, 0)

    def testRasterTileWorkflow(self):
        """Upload a raster, then check that the tile request is not empty"""
        testfile = "hotmaps-cdd_curr_adapted.tif"
        response = self.import_testdata(testfile)

        args = self.TILE_PARAMETERS
        args["layers"] = testfile
        response = self.client.get("api/wms", query_string=self.TILE_PARAMETERS)
        self.assertStatusCodeEqual(response, 200)
        self.assertGreater(len(response.data), 0)
        Image.open(io.BytesIO(response.data))
        # test that we received an image


class WMSGetFeatureInfoTest(BaseApiTest):
    """Test the wms GetMap endpoint"""

    INFO_PARAMETERS = {
        "REQUEST": "GetFeatureInfo",
        "SERVICE": "WMS",
        "SRS": "EPSG:4326",
        "STYLES": "",
        "TRANSPARENT": "true",
        "VERSION": "1.1.1",
        "FORMAT": "image/png",
        "BBOX": "-2.8124638200947287,50.958439559875124"
        ","
        "2.801549851780272,51.67597427003148",
        "HEIGHT": "209",
        "WIDTH": "1022",
        "LAYERS": "nuts.zip",
        "QUERY_LAYERS": "nuts.zip",
        "INFO_FORMAT": "application/json",
        "X": "343.99341364924635",
        "Y": "134.00370991511704",
    }

    def testGetInfoGermany(self):
        """Post a vector and retrieve it by the WMS endpoint as geojson file."""
        testfile = "nuts.zip"
        test_data, testfile_content = self.get_testformdata(testfile)
        response = self.client.post(
            "api/geofile/",
            data=test_data,
            content_type="multipart/form-data",
            follow_redirects=True,
        )
        self.assertStatusCodeEqual(response, 200)

        response = self.client.get("/api/wms", query_string=self.INFO_PARAMETERS)
        self.assertStatusCodeEqual(response, 200)
        json_response = json.loads(response.data)
        self.assertIn("features", json_response)
        self.assertEqual(len(json_response["features"]), 1)


WMS_VERSION = "1.3.0"


class TestWMSLibCompliance(BaseIntegrationTest):
    def setUp(self, *args, **kwargs):
        """Create the wms endpoint base on the parent self.api_url"""
        super().setUp(*args, **kwargs)
        self.wms_url = self.api_url + "/wms"

    def test_wms_content(self):
        """Verify that the content of the wms can be listed"""
        wms = WebMapService(self.wms_url, version=WMS_VERSION)
        self.assertNotEqual(len(wms.contents), 0)
