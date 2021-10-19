import unittest

from . import utils


class WMSHelperTest(unittest.TestCase):
    def testLayerSplit(self):
        raw_l = "a,b,c"
        parsed_list = utils.parse_list(raw_l)
        self.assertEqual(
            parsed_list,
            ["a", "b", "c"],
        )

    def testLayerSplitWithComma(self):
        raw_l = "a%2C,b,c"
        parsed_list = utils.parse_list(raw_l)
        self.assertEqual(
            parsed_list,
            ["a,", "b", "c"],
        )
