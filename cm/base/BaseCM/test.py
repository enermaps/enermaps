import json
import os
import unittest

from BaseCM.cm_input import validate_selection
from BaseCM.cm_output import CMOutput

CURRENT_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
TESTDATA_DIR = os.path.join(CURRENT_FILE_DIR, "testdata")


def get_json_testdata(filename: str):
    """Return the json test file"""
    filepath = os.path.join(TESTDATA_DIR, filename)
    with open(filepath) as fd:
        return json.load(fd)


class TestSelectionValidation(unittest.TestCase):
    def get_raster_path(self, raster_name: str):
        """Returns the path to the raster file based on the raster name."""
        raster_path = os.path.join(TESTDATA_DIR, raster_name)
        path_exists = os.path.isfile(raster_path)
        self.assertTrue(path_exists, msg=raster_path)
        return raster_path

    def testNoCountDetected(self):
        """Check the validity for selection without any count."""
        selection_data = get_json_testdata(filename="test_cm_input_no_count.json")
        selection = selection_data["selection"]
        raster = self.get_raster_path(raster_name=selection_data["layers"][0])
        selection_validity, response = validate_selection(
            selection=selection,
            raster=raster,
        )
        self.assertFalse(selection_validity)

    def testCountDetected(self):
        """Check the validity for selection with count."""
        selection_data = get_json_testdata(filename="test_cm_input_max_count.json")
        selection = selection_data["selection"]
        raster = self.get_raster_path(raster_name=selection_data["layers"][0])
        selection_validity, response = validate_selection(
            selection=selection,
            raster=raster,
        )
        self.assertTrue(selection_validity)

    def testMaxCountDetected(self):
        """Check the validity for selection with a limited number of count."""
        selection_data = get_json_testdata(filename="test_cm_input_max_count.json")
        selection = selection_data["selection"]
        raster = self.get_raster_path(raster_name=selection_data["layers"][0])

        selection_validity, response = validate_selection(
            selection=selection,
            raster=raster,
            max_count=1,
        )
        self.assertFalse(selection_validity)
        selection_validity, response = validate_selection(
            selection=selection,
            raster=raster,
            max_count=3,
        )
        self.assertTrue(selection_validity)


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
