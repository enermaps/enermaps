import unittest
import io
import tempfile
import shutil
import json
import main
import os

def get_testdata(filename):
    """Return the absolute location of the filename in the testdatadir
    """
    testdata_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testdata")
    return os.path.join(testdata_dir, filename)

class TifGeofileTest(unittest.TestCase):
    def setUp(self):
        self.flask_app = main.app
        self.flask_app.config['TESTING'] = True
        self.flask_app.config['UPLOAD_DIR'] = tempfile.mkdtemp()
        self.client = self.flask_app.test_client()
        self.assertEqual(self.flask_app.debug, False)

    def tearDown(self):
        shutil.rmtree(self.flask_app.config['UPLOAD_DIR'])

    def get_testformdata(self, testfile):
        with open(get_testdata(testfile), "rb") as f:
            testfile_content = f.read()
            testfile_io = io.BytesIO(testfile_content)
            test_data =  {
                    "file": (testfile_io, testfile),
                    }
        return test_data, testfile_content

    def testFileEscape(self):
        testfile = "hotmaps-cdd_curr_adapted.tif"
        test_data, testfile_content = self.get_testformdata(testfile)

    def testTif(self):
        """Verify raster upload in geotiff format, listing and retrieval
        """
        testfile = "hotmaps-cdd_curr_adapted.tif"
        test_data, testfile_content = self.get_testformdata(testfile)
        response = self.client.post('geofile', data=test_data, content_type='multipart/form-data')
        self.assertEqual(response.status, "200 OK")
        response.close()

        response = self.client.get("/geofile")
        self.assertEqual(response.status, "200 OK")
        json_content = json.loads(response.data)
        self.assertIn(testfile, json_content['files'])
        response.close()

        response = self.client.get("/geofile/" + testfile)
        self.assertEqual(response.status, "200 OK")
        self.assertEqual(response.data, testfile_content)
        response.close()


if __name__ == "__main__":
    unittest.main()
