import sys
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


if __name__ == "__main__":
    testsuite = get_testsuite(TestSettings, TestGeofileTools, TestAreasTools)
    runner = unittest.TextTestRunner(verbosity=2)
    test_results = runner.run(testsuite)
    if not test_results.wasSuccessful():
        sys.exit(1)
