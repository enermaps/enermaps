import unittest

from tools.test_areas import TestAreasTools
from tools.test_geofile import TestGeofileTools
from tools.test_settings import TestSettings


def get_testsuite(*testcases: unittest.TestCase):
    def import_testcase(tests_class: unittest.TestCase):
        return unittest.TestLoader().loadTestsFromTestCase(tests_class)

    test_case = [import_testcase(testcase) for testcase in testcases]

    test_suite = unittest.TestSuite(test_case)

    return test_suite


testsuite = get_testsuite(TestSettings, TestGeofileTools, TestAreasTools)

if __name__ == "__main__":
    unittest.TextTestRunner().run(testsuite)
