import unittest


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
        # Change given testlist into a TestSuite
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