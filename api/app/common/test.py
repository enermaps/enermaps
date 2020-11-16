import io
import shutil
import subprocess  # nosec
import tempfile
import unittest

from app import create_app
from app.common import filepath


def skipUnlessDockerComposeCanBeExecuted(f):
    """This decorator can be used to skip integration test
    when the docker-compose executable was not found.
    """
    try:
        subprocess.check_call(["docker-compose", "--version"], shell=False)  # nosec
    except FileNotFoundError:
        return unittest.skip("Couldn't find docker-compose, skipping test")
    return lambda func: func


class BaseApiTest(unittest.TestCase):
    def setUp(self):
        """Before each test:
        * set the TESTING to true
        * set the upload directory to a temporary directory
        * ensure we don't run the test in debug
        """
        self.flask_app = create_app(testing=True)
        self.upload_dir = tempfile.mkdtemp()
        self.flask_app.config["UPLOAD_DIR"] = self.upload_dir
        self.client = self.flask_app.test_client()
        self.assertEqual(self.flask_app.debug, False)

    def tearDown(self):
        """After each test, cleanup the upload directory"""
        shutil.rmtree(self.flask_app.config["UPLOAD_DIR"])

    def get_testformdata(self, testfile, testfile_name=None):
        """Return"""
        with open(filepath.get_testdata_path(testfile), "rb") as f:
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
        self.assertStatusCodeEqual(response, 200)
        return response

    def import_nuts(self):
        for nuts_level in range(4):
            filename = "nuts{!s}.zip".format(nuts_level)
            self.import_testdata(filename)

    def assertStatusCodeEqual(self, response, status_code):
        """Assert that a flask client test status code is
        equal to the status_code
        """
        self.assertEqual(response.status_code, status_code, response.data)
