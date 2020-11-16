import io
import json
import unittest
import zipfile

from app.common.test import BaseApiTest
from app.models.geofile import RasterLayer


class VectorGeofileTest(BaseApiTest):
    def testUploadThenDownload(self):
        testfile = "nuts.zip"
        test_data, initial_data = self.get_testformdata(testfile)
        response = self.client.post(
            "api/geofile/", data=test_data, content_type="multipart/form-data"
        )
        self.assertEqual(response.status, "200 OK", response.data)
        resp = self.client.get("api/geofile/" + testfile)
        initial_zip = zipfile.ZipFile(io.BytesIO(initial_data))
        returned_zip = zipfile.ZipFile(io.BytesIO(resp.data))
        initial_files = initial_zip.filelist
        returned_files = returned_zip.filelist
        self.assertEqual(len(initial_files), len(returned_files))

        def get_filename(zipinfo):
            return zipinfo.filename

        initial_filenames = set(map(get_filename, initial_files))
        returned_filenames = set(map(get_filename, returned_files))
        self.assertEqual(initial_filenames, returned_filenames)

    def testUploadShapefile(self):
        testfile = "nuts.zip"
        test_data, _ = self.get_testformdata(testfile)
        response = self.client.post(
            "api/geofile/", data=test_data, content_type="multipart/form-data"
        )
        self.assertStatusCodeEqual(response, 200)

        test_data, _ = self.get_testformdata(testfile)
        response = self.client.get("api/geofile/")
        self.assertStatusCodeEqual(response, 200)
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
        self.assertStatusCodeEqual(response, 200)
        response = self.client.get("api/geofile/")
        self.assertStatusCodeEqual(response, 200)
        json_content = json.loads(response.data)
        self.assertIn(testfile_name, json_content["files"])

    def testHiddenFile(self):
        """Hidden shapefile are a bit special, they don't appear in the listing but are
        still available when the geofile name is known.
        """
        testfile = "hotmaps-cdd_curr_adapted.tif"
        testfile_name = ".test.tif"
        test_data, _ = self.get_testformdata(testfile, testfile_name=testfile_name)
        response = self.client.post(
            "api/geofile/", data=test_data, content_type="multipart/form-data"
        )
        self.assertStatusCodeEqual(response, 200)
        response = self.client.get("api/geofile/")
        self.assertStatusCodeEqual(response, 200)
        json_content = json.loads(response.data)
        self.assertNotIn(testfile_name, json_content["files"])
        self.assertEqual(json_content["files"], [])

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
        self.assertStatusCodeEqual(response, 200)

        response = self.client.get("api/geofile/")
        self.assertStatusCodeEqual(response, 200)
        json_content = json.loads(response.data)
        self.assertIn(testfile, json_content["files"])

        response = self.client.get("api/geofile/" + testfile)
        self.assertStatusCodeEqual(response, 200)
        self.assertEqual(response.data, testfile_content)
        self.assertEqual(response.mimetype, RasterLayer.MIMETYPE[0])


if __name__ == "__main__":
    unittest.main()
