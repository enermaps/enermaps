import json
import os
import unittest

from BaseCM.cm_output import CMOutput

CURRENT_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
TESTDATA_DIR = os.path.join(CURRENT_FILE_DIR, "testdata")


def get_json_testdata(filename: str):
    """Return the json test file"""
    filepath = os.path.join(TESTDATA_DIR, filename)
    with open(filepath) as fd:
        return json.load(fd)


class TestSchema(unittest.TestCase):
    def testLoad(self):
        """Test the load and the validation of json"""
        output_schema = CMOutput()
        json_testdata = get_json_testdata("marshmallow.json")
        out = output_schema.load(data=json_testdata)
        self.assertGreater(len(out), 0)

    def testLongLoad(self):
        """Test the load and the validation of long json"""
        output_schema = CMOutput()
        json_testdata = get_json_testdata("test.json")
        out = output_schema.load(data=json_testdata)
        self.assertGreater(len(out), 0)

    def testEmptyLoad(self):
        """Test the load and the validation of empty json"""
        output_schema = CMOutput()
        json_testdata = get_json_testdata("test_empty.json")
        out = output_schema.load(data=json_testdata)
        self.assertGreater(len(out), 0)
