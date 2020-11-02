import io
import os
import shutil
import tempfile
import unittest

import app.app as app_module


def get_testdata(filename):
    """Return the absolute location of the filename in the testdatadir"""
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    testdata_dir = os.path.join(os.path.dirname(current_file_dir), "testdata")
    return os.path.join(testdata_dir, filename)


class BaseApiTest(unittest.TestCase):
    def setUp(self):
        """Before each test:
        * set the TESTING to true
        * set the upload directory to a temporary directory
        * ensure we don't run the test in debug
        """
        self.flask_app = app_module.app
        self.flask_app.config["TESTING"] = True
        self.upload_dir = tempfile.mkdtemp()
        self.flask_app.config["UPLOAD_DIR"] = self.upload_dir
        self.client = self.flask_app.test_client()
        self.assertEqual(self.flask_app.debug, False)

    def tearDown(self):
        """After each test, cleanup the upload directory"""
        shutil.rmtree(self.flask_app.config["UPLOAD_DIR"])

    def get_testformdata(self, testfile, testfile_name=None):
        """Return"""
        with open(get_testdata(testfile), "rb") as f:
            testfile_content = f.read()
            testfile_io = io.BytesIO(testfile_content)
            if not testfile_name:
                testfile_name = testfile
            test_data = {"file": (testfile_io, testfile_name)}
        return test_data, testfile_content

    def import_testdata(self, testfile_name):
        """Helper function that upload the testfile to the api."""
        form_content, _ = self.get_testformdata(testfile_name)
        self.client.post("/api/geofile")
        response = self.client.post(
            "api/geofile/", data=form_content, content_type="multipart/form-data"
        )
        self.assertEqual(response.status, "200 OK", response.data)
        return response

    def import_nuts(self):
        for nuts_level in range(4):
            filename = "nuts{!s}.zip".format(nuts_level)
            self.import_testdata(filename)
