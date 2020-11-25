import logging
from unittest.mock import patch

from app.common.test import BaseApiTest
from app.models.calculation_module import from_registration_string, list_cms

CM_STRING_NO_INFO = "[CMName]"
CM_STRING_BAD_JSON = "[CMName cm_info={]"
CM_STRING0 = 'CMName [cm_info={"doc": "doc"}]'
CM_STRING1 = 'CM Name [cm_info={"doc": "doc"}]'


class TestCMS(BaseApiTest):
    @patch("kombu.utils.functional.sleep", return_value=None)
    def testListCMTimeout(self, _):
        """Test that a non reachable redis will
        Just return an empty list of cms.
        """
        with self.assertLogs(level=logging.ERROR):
            cms = list_cms()
        self.assertEquals(len(cms), 0)

    def testSuccessWhenParsingWithSpace(self):
        cm = from_registration_string(CM_STRING1)
        self.assertEqual(cm.__doc__, "doc")

    def testFailWhenParseWrongCMInfo(self):
        """Test some parsing error of the info string"""
        with self.assertRaises(Exception):
            from_registration_string("[")
        with self.assertRaises(Exception):
            from_registration_string("[]")
        with self.assertRaises(Exception):
            # String missing the cm_info
            from_registration_string(CM_STRING_NO_INFO)

    def testSuccessWhenParsing(self):
        """Test a valid cm info parsing."""
        cm = from_registration_string(CM_STRING0)
        self.assertEqual(cm.__doc__, "doc")
