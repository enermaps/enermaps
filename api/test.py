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
        self.upload_dir = tempfile.mkdtemp()
        self.flask_app.config['UPLOAD_DIR'] = self.upload_dir
        self.client = self.flask_app.test_client()
        self.assertEqual(self.flask_app.debug, False)

    def tearDown(self):
        shutil.rmtree(self.flask_app.config['UPLOAD_DIR'])

    def get_testformdata(self, testfile, testfile_name=None):
        with open(get_testdata(testfile), "rb") as f:
            testfile_content = f.read()
            testfile_io = io.BytesIO(testfile_content)
            if not testfile_name:
                testfile_name = testfile
            test_data =  {
                    "file": (testfile_io, testfile_name),
                    }
        return test_data, testfile_content

    def testFileEscapePost(self):
        testfile = "hotmaps-cdd_curr_adapted.tif"
        test_data, testfile_content = self.get_testformdata(testfile, testfile_name="../test.tif")
        response = self.client.post('/geofile', data=test_data, content_type='multipart/form-data')
        self.assertEqual(response.status, "404 NOT FOUND", response.data)
        #raise Exception(os.listdir(self.upload_dir + "/user"))
        
    def testTifUnicode(self):
        testfile = "hotmaps-cdd_curr_adapted.tif"
        testfile_name = "⎈. tif"
        test_data, testfile_content = self.get_testformdata(testfile, testfile_name=testfile_name)
        response = self.client.post('/geofile', data=test_data, content_type='multipart/form-data')
        self.assertEqual(response.status, "200 OK", response.data)
        response = self.client.get('/geofile')
        self.assertEqual(response.status, "200 OK", response.data)
        json_content = json.loads(response.data)
        self.assertIn(testfile_name, json_content['files'])

    def testTif(self):
        """Verify raster upload in geotiff format, listing and retrieval
        """
        testfile = "hotmaps-cdd_curr_adapted.tif"
        test_data, testfile_content = self.get_testformdata(testfile)
        response = self.client.post('/geofile', data=test_data, content_type='multipart/form-data')
        self.assertEqual(response.status, "200 OK", response.data)
        response.close()

        response = self.client.get("/geofile")
        self.assertEqual(response.status, "200 OK", response.data)
        json_content = json.loads(response.data)
        self.assertIn(testfile, json_content['files'])
        response.close()

        response = self.client.get("/geofile/" + testfile)
        self.assertEqual(response.status, "200 OK", response.data)
        self.assertEqual(response.data, testfile_content)
        response.close()


if __name__ == "__main__":
    unittest.main()
