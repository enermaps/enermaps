import json
import unittest

from app.common.test import BaseApiTest
from app.models.geofile import RasterLayer


class VectorGeofileTest(BaseApiTest):
    def testUploadShapefile(self):
        testfile = "nuts.zip"
        test_data, _ = self.get_testformdata(testfile)
        response = self.client.post(
            "api/geofile/", data=test_data, content_type="multipart/form-data"
        )
        self.assertEqual(response.status, "200 OK", response.data)

        test_data, _ = self.get_testformdata(testfile)
        response = self.client.get("api/geofile/")
        self.assertEqual(response.status, "200 OK", response.data)
        json_content = json.loads(response.data)
        self.assertIn(testfile, json_content["files"])

    def testUploadBadZip(self):
        testfile = "hotmaps-cdd_curr_adapted.tif"
        test_data, _ = self.get_testformdata(testfile, testfile_name="test.zip")
        response = self.client.post(
            "api/geofile/", data=test_data, content_type="multipart/form-data"
        )
        self.assertEqual(response.status, "400 BAD REQUEST", response.data)


class TifGeofileTest(BaseApiTest):
    def testFileEscapePost(self):
        testfile = "hotmaps-cdd_curr_adapted.tif"
        test_data, _ = self.get_testformdata(testfile, testfile_name="../test.tif")
        response = self.client.post(
            "api/geofile/", data=test_data, content_type="multipart/form-data"
        )
        self.assertEqual(response.status, "404 NOT FOUND", response.data)

    def testTifUnicode(self):
        testfile = "hotmaps-cdd_curr_adapted.tif"
        testfile_name = "⎈.tif"
        test_data, _ = self.get_testformdata(testfile, testfile_name=testfile_name)
        response = self.client.post(
            "api/geofile/", data=test_data, content_type="multipart/form-data"
        )
        self.assertEqual(response.status, "200 OK", response.data)
        response = self.client.get("api/geofile/")
        self.assertEqual(response.status, "200 OK", response.data)
        json_content = json.loads(response.data)
        self.assertIn(testfile_name, json_content["files"])

    def testUploadWithoutProjection(self):
        """We refuse to work with geotiff that don't contain a projection, they
        can get us in trouble later when serving them as tile.
        """
        testfile = "no_projection.tif"
        test_data, _ = self.get_testformdata(testfile)
        response = self.client.post(
            "/api/geofile/", data=test_data, content_type="multipart/form-data"
        )
        self.assertEqual(response.status, "400 BAD REQUEST", response.data)

    def testTifUploadAndRetrieval(self):
        """Verify raster upload in geotiff format, listing and retrieval"""
        testfile = "hotmaps-cdd_curr_adapted.tif"
        test_data, testfile_content = self.get_testformdata(testfile)
        response = self.client.post(
            "api/geofile/", data=test_data, content_type="multipart/form-data"
        )
        self.assertEqual(response.status, "200 OK", response.data)

        response = self.client.get("api/geofile/")
        self.assertEqual(response.status, "200 OK", response.data)
        json_content = json.loads(response.data)
        self.assertIn(testfile, json_content["files"])

        response = self.client.get("api/geofile/" + testfile)
        self.assertEqual(response.status, "200 OK", response.data)
        self.assertEqual(response.data, testfile_content)
        self.assertEqual(response.mimetype, RasterLayer.MIMETYPE[0])


if __name__ == "__main__":
    unittest.main()
