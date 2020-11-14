from app.common.test import BaseApiTest
from app.models.calculation_module import list_cms, from_registration_string

CM_STRING_NO_INFO = "[CMName]"
CM_STRING_BAD_JSON = "[CMName cm_info={]"
CM_STRING0 = 'CMName [cm_info={"doc": "doc"}]'

class TestCMS(BaseApiTest):
    def testListCMTimeout(self):
        """Test that a non reachable redis will
        Just return an empty list of cms.
        """
        cms = list_cms()
        self.assertEquals(len(cms), 0)

    def testFailWhenParseWrongCMInfo(self):
        """Test some parsing error of the info string
        """
        with self.assertRaises(Exception):
            from_registration_string("[")
        with self.assertRaises(Exception):
            from_registration_string("[]")
        with self.assertRaises(Exception):
            # String missing the cm_info
            from_registration_string(CM_STRING_NO_INFO)
        with self.assertRaises(Exception):
            # String missing the cm_info
            from_registration_string(CM_STRING_NO_INFO)

    def testSuccessWhenParsing(self):
        """Test a valid cm info parsing.
        """
        cm = from_registration_string(CM_STRING0)
        self.assertEqual(cm.__doc__, "doc")

