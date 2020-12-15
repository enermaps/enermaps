import unittest
import json

import output

class TestSchema(unittest.TestCase):
    def testLoad(self):
        cm_output_schema = output.CMOutput()

        with open("test.json") as fd:
            loaded = cm_output_schema.load(json.load(fd))
        self.assertEqual(len(loaded), 3)

    def testLoadEmpty(self):
        cm_output_schema = output.CMOutput()

        with open("test_empty.json") as fd:
            loaded = cm_output_schema.load(json.load(fd))
        self.assertEqual(len(loaded), 3)

    def testDumpJSONSchema(self):
        json_schema = output.CMOutput.as_json_schema()
        with open("schema.json", "w") as fd:
            json.dump(json_schema, fd)
