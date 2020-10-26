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
        self.flask_app = app_module.app
        self.flask_app.config["TESTING"] = True
        self.upload_dir = tempfile.mkdtemp()
        self.flask_app.config["UPLOAD_DIR"] = self.upload_dir
        self.client = self.flask_app.test_client()
        self.assertEqual(self.flask_app.debug, False)

    def tearDown(self):
        shutil.rmtree(self.flask_app.config["UPLOAD_DIR"])
