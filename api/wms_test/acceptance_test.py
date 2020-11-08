"""Acceptance test for the compatibility of enermaps2 wms with owslib.

This test will call the WebMapService and check that it can list its content
"""
import argparse
import sys
import unittest
from typing import Text

from owslib.wms import WebMapService


DEFAULT_URL = "http://127.0.0.1:7000/api/wms"
DEFAULT_WMS_VERSION = "1.1.1"


class TestWMSLibCompliance(unittest.TestCase):
    def __init__(self, name: Text, url: Text, version: Text):
        """Initialize the testcase, allowing options to be passed.

        url: the url of the wms as a string
        version: the version of the wms (1.1.1 or 1.3.0 are the most common versions)
        """
        self.url = url
        self.version = version
        super().__init__(name)

    def test_wms_content(self):
        """Verify that the content of the wms can be listed"""
        wms = WebMapService(self.url, version=self.version)
        self.assertNotEqual(len(wms.contents), 0)


def get_parser():
    """Return an argparse instance allowing command line argument to be parsed.
    Those cover the url and the wms version.
    """
    parser = argparse.ArgumentParser(__file__)
    parser.add_argument(
        "-u", "--url", default=DEFAULT_URL, help="url of the wms to be queried"
    )
    parser.add_argument(
        "-w",
        "--wms-version",
        default=DEFAULT_WMS_VERSION,
        help="url of the wms to be queried",
    )
    return parser


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    suite = unittest.TestSuite()
    wmsLibTest = TestWMSLibCompliance("test_wms_content", args.url, args.wms_version)
    suite = unittest.TestSuite()
    suite.addTest(wmsLibTest)
    result = unittest.TextTestRunner().run(suite)
    if not result.wasSuccessful():
        sys.exit(1)
