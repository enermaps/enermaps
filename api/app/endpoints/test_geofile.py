import io
import json
import unittest

from app.common.test import BaseApiTest, get_testdata


class TifGeofileTest(BaseApiTest):
    def get_testformdata(self, testfile, testfile_name=None):
        with open(get_testdata(testfile), "rb") as f:
            testfile_content = f.read()
            testfile_io = io.BytesIO(testfile_content)
            if not testfile_name:
                testfile_name = testfile
            test_data = {"file": (testfile_io, testfile_name)}
        return test_data, testfile_content

    def testFileEscapePost(self):
        testfile = "hotmaps-cdd_curr_adapted.tif"
        test_data, _ = self.get_testformdata(
            testfile, testfile_name="../test.tif"
        )
        response = self.client.post(
            "api/geofile/", data=test_data, content_type="multipart/form-data"
        )
        self.assertEqual(response.status, "404 NOT FOUND", response.data)
        # raise Exception(os.listdir(self.upload_dir + "/user"))

    def testTifUnicode(self):
        testfile = "hotmaps-cdd_curr_adapted.tif"
        testfile_name = "⎈. tif"
        test_data, _ = self.get_testformdata(
            testfile, testfile_name=testfile_name
        )
        response = self.client.post(
            "api/geofile/", data=test_data, content_type="multipart/form-data"
        )
        self.assertEqual(response.status, "200 OK", response.data)
        response = self.client.get("api/geofile/")
        self.assertEqual(response.status, "200 OK", response.data)
        json_content = json.loads(response.data)
        self.assertIn(testfile_name, json_content["files"])

    def testUploadWithoutProjection(self):
        """We refuse to work with geotiff that don't contain a projection, they can get us in trouble later
        when serving them.
        """
        testfile = "no_projection.tif"
        test_data, _ = self.get_testformdata(testfile)
        response = self.client.post(
            "/api/geofile/", data=test_data, content_type="multipart/form-data"
        )
        self.assertEqual(response.status, "400 BAD REQUEST", response.data)

    def testTifUploadAndRetrieval(self):
        """Verify raster upload in geotiff format, listing and retrieval
        """
        testfile = "hotmaps-cdd_curr_adapted.tif"
        test_data, testfile_content = self.get_testformdata(testfile)
        response = self.client.post(
            "api/geofile/", data=test_data, content_type="multipart/form-data"
        )
        self.assertEqual(response.status, "200 OK", response.data)
        response.close()

        response = self.client.get("api/geofile/")
        self.assertEqual(response.status, "200 OK", response.data)
        json_content = json.loads(response.data)
        self.assertIn(testfile, json_content["files"])
        response.close()

        response = self.client.get("api/geofile/" + testfile)
        self.assertEqual(response.status, "200 OK", response.data)
        self.assertEqual(response.data, testfile_content)
        response.close()


if __name__ == "__main__":
    unittest.main()
