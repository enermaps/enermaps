"""Simplified entrypoint for discovering and running all test of the project
"""
import sys
import unittest

import app  # NOQA

if __name__ == "__main__":
    loader = unittest.TestLoader()
    tests = loader.discover("app/")
    testRunner = unittest.runner.TextTestRunner()
    result = testRunner.run(tests)
    if not result.wasSuccessful():
        sys.exit(1)
