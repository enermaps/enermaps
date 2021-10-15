"""Common classes used as base for the integration test
and the unittest.
"""
import io
import logging
import os
import shutil
import tempfile
import time
import unittest

import requests
import urllib3

from app import create_app


class BaseTest(unittest.TestCase):
    @classmethod
    def get_testdata_path(cls, filename):
        """Return the absolute location of the filename in the testdatadir"""
        current_file_dir = os.path.dirname(os.path.abspath(__file__))
        testdata_dir = os.path.join(os.path.dirname(current_file_dir), "testdata")
        return os.path.join(testdata_dir, filename)


class BaseApiTest(BaseTest):
    def setUp(self):
        """Before each test:
        * set the TESTING to true
        * set the upload directory to a temporary directory
        * ensure we don't run the test in debug
        """
        self.flask_app = create_app(testing=True)
        self.wms_cache_dir = tempfile.mkdtemp()
        self.cm_outputs_dir = tempfile.mkdtemp()
        self.flask_app.config["WMS_CACHE_DIR"] = self.wms_cache_dir
        self.flask_app.config["CM_OUTPUTS_DIR"] = self.cm_outputs_dir
        self.client = self.flask_app.test_client()
        self.client.follow_redirect = True
        self.assertEqual(self.flask_app.debug, False)

    def tearDown(self):
        """After each test, cleanup the upload directory"""
        shutil.rmtree(self.flask_app.config["WMS_CACHE_DIR"])
        shutil.rmtree(self.flask_app.config["CM_OUTPUTS_DIR"])

    def prepare_file_upload(self, filename, dest_filename=None):
        """Return the data corresponding to a file upload"""
        with open(self.get_testdata_path(filename), "rb") as f:
            content = f.read()
            file_io = io.BytesIO(content)
            if not dest_filename:
                dest_filename = filename

            test_data = {"file": (file_io, dest_filename)}

        return test_data, content

    def assertStatusCodeEqual(self, response, status_code):
        """Assert that a flask client test status code is
        equal to the status_code
        """
        self.assertEqual(response.status_code, status_code, response.data)


def labeledTest(*labels):
    """This decorator mark a class as an integrationTest
    this is used in the test call for filtering integrationTest
    and unittest.
    We mark the difference by the usage of service dependency:
    * An unittest can run without additional services.
    * An integration test need additional services (such as
      redis or postgres).

    Usage:

        @labeledTest("integration")
        class FakeOutputTest(BaseApiTest):
            pass
    """

    def wrapper(cl):
        cl._label = set(labels)
        return cl

    return wrapper


class LabelTestRunner(unittest.runner.TextTestRunner):
    """This testrunner accept a list of whitelist_labels,
    It will run all test without a label if no label is
    specified. If a label is specified, all testcase class
    decorated with labeledTest and having a label in the
    whitelist_labels will be ran.
    """

    def __init__(self, selection_labels=[], *args, **kwargs):
        self.selection_labels = set(*selection_labels)

        super(LabelTestRunner, self).__init__(*args, **kwargs)

    @classmethod
    def flatten_tests(cls, suite):
        """Iterate through the test in a test suite. It will
        yield individual tests by flattening the suite into
        a list of tests.
        """
        for test in suite:
            if isinstance(test, unittest.TestSuite):
                for t in cls.flatten_tests(test):
                    yield t
            else:
                yield test

    def run(self, testlist):
        """Change given testlist into a TestSuite.
        And then run all the tests of the TestSuite
        without (or with the right) label.
        """

        # Create TestSuite instance
        suite = unittest.TestSuite()

        # Add each test in testlist, apply skip mechanism if necessary
        for test in self.flatten_tests(testlist):

            if hasattr(test, "_label"):
                matched_label = test._label.intersection(self.selection_labels)
                if matched_label:
                    suite.addTest(test)
            elif not self.selection_labels:
                suite.addTest(test)

        # Resume normal TextTestRunner function with the created test suite
        return super().run(suite)


DEFAULT_API_URL = "http://127.0.0.1:7000"


@labeledTest("integration")
class BaseIntegrationTest(BaseTest):
    def wait_for_reachability(self, max_retry=20, wait_time=3):
        """Wait for the api to be reachable by poking its healthz endpoint"""
        retry = 0
        logging.info("Waiting for the api to be reachable")
        while retry <= max_retry:
            try:
                resp = self.session.get(self.url + "/healthz")
            except (
                urllib3.exceptions.MaxRetryError,
                urllib3.exceptions.TimeoutError,
                requests.exceptions.ConnectionError,
                requests.exceptions.RequestException,
            ):
                logging.info(".")
            else:
                if resp.ok:
                    return True
            retry += 1
            time.sleep(wait_time)
        return False

    def setUp(self, *args, **kwargs):
        self.url = os.environ.get("API_URL", DEFAULT_API_URL)
        self.api_url = self.url + "/api"
        self.session = requests.Session()
        super().__init__(*args, **kwargs)
        if not self.wait_for_reachability():
            logging.error("API is not reachable after max retries")
